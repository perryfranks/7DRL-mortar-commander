from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
import render_functions
import sys
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    """
    The game engine. handles basically everything including rendering within the console already set up.
    :param player: the main player object to be the player's input entity throughout the game
    :type player: Player
    :param fov: whether the game renders the players field of view
    :type fov: bool
    """
    # TODO: having fov off may cause errors. Experiment and fix
    # Yep it casues the whole screen to be black
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor, fov: bool = True):
        self.message_log = MessageLog()
        self.player = player
        self.mouse_location = (0, 0)
        self.hasFov = fov

    def handle_entity_turns(self) -> None:
        """
        Calls the entity.ai.perform() of all entities that have that component minus the player
        """
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def handle_enemy_turns(self) -> None:
        """
        Call the perform action for all entities that have an ai component.
Note that currently this calls handle_entity_turns and acts on all entities minus the player
        """
        self.handle_entity_turns()

    def update_fov(self, sight_radius: int = 8) -> None:
        """
        Recompute the visible area based on the players point of view.
        if hasFov is false then this will not act on anything
        """
        if not self.hasFov:
            return

        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=sight_radius,
        )
        # If a tile is visible it should be added to explored
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        """
        calls the render functions for the different components of the game
        includes logic about placement of elements.
        Components include the: map, message log, health bars and so on
        :param console: tcod console that will handle lots of the heavy lifting
        :type console: Console (libtcod class)
        :return: None
        """
        try:
            self.game_map.render(console)
        except ValueError as e:
            print(
                "ValueError raised when trying to render game map. This maybe because the map is bigger than the  "
                "console"
            )
            print(e)
            sys.exit(exceptions.ErrorCodes.CRITICAL)
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        # render the health bar of the player
        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        # display the current dungeon level
        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
