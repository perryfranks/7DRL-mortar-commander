from __future__ import annotations

import random
from typing import List, Optional, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction, EnemyPickupSuppliesAction
from components.consumable import Supplies, Consumable

if TYPE_CHECKING:
    from entity import Actor, Entity


class BaseAI(Action):
    """
    Base AI only implements the simple pathfinding function get_path_to()
    When something will apply to all entities with AI (most likely anything that moves) add it here

    When extending this class the first step is implementing perform(). This defines what the entity will actually do
    """

    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target_class position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

            # Create a graph from the cost array and pass that graph to a new pathfinder.
            graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
            pathfinder = tcod.path.Pathfinder(graph)
            pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

            # Compute the path to the destination and remove the starting point
            path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

            return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    """
        Defines basic enemy actions of moving to the player. If the player is within 1 tile attack them
        NOTE: an enemies bump attack is defined here
    """

    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            # our first hack attempt
            if distance == 0:
                return None
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        return WaitAction(self.entity).perform()


class EnemySupplyScavenger(HostileEnemy):
    """
        Basically the HostileEnemy but will go for the nearest supplies instead of the player
    """

    def get_target(self) -> Optional[Supplies]:
        """
        Get the nearest supplies to target_class
        :return: Entity to target_class. From there you can extract x,y.
                If return is None that means there are no more supplies on the map
        """
        return self.engine.game_map.get_closest_consumable(
            self.entity, Supplies
        )

    def get_supplies(self, supplies: Supplies) -> None:
        # ToDo: untested
        """
        Handle the enemy grabbing a supply consumable. This will remove it from the map.
        :param supplies: the supply entity that is going to be consumed
        :return: None
        """
        # add the supplies to the tally
        EnemyPickupSuppliesAction(self.entity, supplies.value)
        # remove from the map
        self.engine.game_map.entities.remove(supplies)

    def perform(self) -> None:
        # Get the nearest supplies
        # Grab them if they are within reach

        target = self.get_target() # this also gets the chebyshev dist
        dx = target.parent.x - self.entity.x
        dy = target.parent.y - self.entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance

        # if self.engine.game_map.visible[self.entity.x, self.entity.y]:
        if distance == 0:
            # grab the supplies I suppose
            return self.get_supplies(target)

        self.path = self.get_path_to(target.parent.x, target.parent.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            return MovementAction(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()

        # This is the safety return
        return WaitAction(self.entity).perform()


class ConfusedEnemy(BaseAI):
    """
    A Confused enemy will stumble around aimlessly for a given number of turns, then revert back to its previous AI.
    If an actor occupies a tile it is randomly moving into, it will attack.
    """

    def __init__(
            self, entity: Actor, previous_ai: Optional[BaseAI], turns_remaining: int
    ):
        super().__init__(entity)
        self.previous_ai = previous_ai
        self.turns_remaining = turns_remaining

    def perform(self) -> None:
        # Revert the AI back to the original state if the effect has run its course.
        if self.turns_remaining <= 0:
            self.engine.message_log.add_message(
                f"The {self.entity.name} is no longer confused."
            )
            self.entity.ai = self.previous_ai
        else:
            # Pick a random direction
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )

            self.turns_remaining -= 1
            # The actor will either try to move or attack in the chosen random direction.
            # Its possible the actor will just bump into the wall, wasting a turn.
            return BumpAction(self.entity, direction_x, direction_y, ).perform()
