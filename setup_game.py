"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import traceback
from typing import Optional

import tcod

import entity_factories
import input_handlers
from config import SAVE_LOCATION
from engine import Engine
from entity import Actor
from game_map import GameWorld
from graphics import color
from graphics.titles import get_welcome_message, TITLE, CREDITS
from save_functions import load_game

# Load the background image and remove the alpha channel.
background_image = tcod.image.load("graphics/menu_background.png")[:, :, :3]


# having these things be hard coded could be fixed.
# Though how do we that and not let the screen break?

# TODO: We could add some polymorphism to this so that any number of functions are called on objects
def game_specific_setup(player: Actor) -> None:
    """
    Set up things specific to the game and not to get the engine/rendering up and running.
    Such as setting the characters inventory.

    :param player: the player or entity to peform the setup functions on
    :type player: Actor
    :returns: Nothing but actions an player object are propagated
    :rtype: None
    """

    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)


def new_game(
        map_width: int = 80,
        map_height: int = 43,
        room_max_size: int = 10,
        room_min_size: int = 6,
        max_rooms: int = 30,
) -> Engine:
    """
    Return a brand new game session as an Engine instance. Parameter defaults are to retain backwards
    compatability with the tcod tutorial game. Should be completely factored, but we can do that later
    The params are passed to the world creation engine.

    :param max_rooms: the maximum number of rooms to have per level.
    :type max_rooms: int
    :param room_min_size: minimum size for each room
    :type room_min_size: int
    :param room_max_size: maximum size for each room
    :type room_max_size: int
    :param map_height:  height of the map that room and corridors are placed in
    :type map_height: int
    :param map_width  width of the map that rooms and corridors are placed in
    :type map_width: int
    :returns: the Engine object to run the game
    """

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,

    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        get_welcome_message(), color.welcome_text
    )

    # Give the player the starting items
    game_specific_setup(player)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            TITLE,
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            CREDITS,
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
                ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
            self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game(SAVE_LOCATION))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
