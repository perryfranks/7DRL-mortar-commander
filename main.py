#! /usr/bin/env python3
import traceback

import tcod
import sys
import exceptions
import graphics.titles
import input_handlers
import setup_game
from graphics import color
from save_functions import save_game
from config import SAVE_LOCATION


# TODO: How will we actually distribute this?
def main(
        screen_width: int,
        screen_height: int,
) -> None:
    """
    Main function that instantiates both the tcod window and game engine (whether by creation or loading a save game)
    this allows us to actually play the game.
    :param screen_width: the width of the screen to create (not how much will be displayed on a single srceen in the
    game)
    :param screen_height: the height of the screen to create
    :return: Nothing. When this function returns it should be the end of the program.
    """

    tileset = tcod.tileset.load_tilesheet(
        "graphics/texture.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title=graphics.titles.TITLE,
            vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    print("the exception clause ran")
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            if exceptions.ErrorCodes.CRITICAL:
                # do not save
                # TODO: this simply printing wont be useful when distributed
                # TODO: how the fuck do we distribute it?
                handler = input_handlers.ErrorScreen()
                handler.on_render(console=root_console)
                context.present(root_console)
                tcod.console_wait_for_keypress(flush=True)
                print("Critical error. Game will not be saved")
            else:
                print("saved game")
                save_game(handler, SAVE_LOCATION)
            raise
        except BaseException:  # Save an any other unexpected exception.
            save_game(handler, SAVE_LOCATION)
            raise


if __name__ == "__main__":
    # If this is to small for what we try to draw then we have a confusing error
    width = 75
    height = 50
    main(screen_width=width, screen_height=height)
