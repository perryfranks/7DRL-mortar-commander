from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING, Set

import numpy as np  # type: ignore
from tcod.console import Console

import tile_room_types
from components.consumable import Consumable

from entity import Entity, Actor, Item

if TYPE_CHECKING:
    from engine import Engine
    # from entity import Entity, Actor, Item


class GameMap:
    """
    Has additional variables of:
    self.tiles
    self.visible
    self.explored
    """

    def __init__(
            self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_room_types.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen & is different from never seen
        # self.visible = np.full(
        #     (width, height), fill_value=False, order="F"
        # )  # Tiles the player can currently see
        # self.explored = np.full(
        #     (width, height), fill_value=False, order="F"
        # )  # Tiles the player has seen & is different from never seen

        self.downstairs_location = (0, 0)

    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this mapping living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    @property
    def consumable_items(self) -> Iterator[Item]:
        """
        Return items with the consumable object attached
        :return:
        """
        yield from (item for item in self.items if item.consumable is not None)

    def get_blocking_entity_at_location(
            self, location_x: int, location_y: int
    ) -> Optional[Entity]:
        """
        Simply checks the block_movement flag for entities in the given spot. The number is
        Only the first blocking entity will be returned. This cannot be used to get the important entities here
        :param location_x:
        :param location_y:
        :return: None or a single entity at the location given
        """
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                return entity

        return None

    def get_blocking_entity_at_location_set(
            self, location_x: int, location_y: int
    ) -> Set:
        e_set = set()
        for entity in self.entities:
            if (
                    entity.blocks_movement
                    and entity.x == location_x
                    and entity.y == location_y
            ):
                e_set.add(entity)

        return e_set

    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        """
        Returns the first actor at the location. Note if there are multiple actors here the one returned is unreliable
        :return: An actor entity. Could be a player or enemy
        """
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    @staticmethod
    def get_distance(entity1: Entity, entity2: Entity) -> int:
        """
        Get distance using Chebyshev distance.
        https://en.wikipedia.org/wiki/Chebyshev_distance
        :param entity1:
        :param entity2:
        :return:
        """
        dx = entity1.x - entity2.x
        dy = entity1.y - entity2.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance
        return distance

    def get_closest_consumable(self, source: Entity, target_class: type[Consumable]) -> Optional[Consumable]:
        """
        Get the closest consumable that matches the target_class. The given coordinates are the
        starting location to calculate distance from.
        """

        # must be careful we match class and not the instance
        # for the every item in the list:
        #   check it is the target_class
        #       calculate distance
        #           if the distance is min keep that as the minimum

        minimum_dist = -1
        minimum_obj = None

        for item in self.consumable_items:
            if isinstance(item.consumable, target_class):
                # This is not running
                dist = self.get_distance(entity1=source, entity2=item)
                if dist <= minimum_dist or minimum_dist < 0:
                    # new contender for closest consumable
                    minimum_obj = item
                    minimum_dist = dist

        return minimum_obj

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside the bounds of this game_map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the game_map.

        If a tile is in the "visible" array, then draw it with the light colors.
        If it isn't, but it's in the explored array then use dark colors.
        Otherwise, the default is SHROUD
        """
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_room_types.SHROUD,
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )

        for entity in entities_sorted_for_rendering:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
