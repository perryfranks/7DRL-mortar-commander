"""
Functionality related to saving and loading the game.
Removed function declarations from other files
"""
import lzma
import pickle

import input_handlers
from engine import Engine


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """if the current event handler has an active engine save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game Saved.")


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file.
    :returns: An Engine that is ready to go, that has same state as when it was saved.
    :rtype: Engine
    """
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine
