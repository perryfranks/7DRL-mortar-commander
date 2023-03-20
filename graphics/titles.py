"""
Constant strings and functions related to the title screen, credits,
or other items that are mostly text strings mostly just printed to the user
"""
import random

TITLE = "MORTAR COMMAND"
# Unfortunately this doesn't render correctly for me. Will shelve for now
title_multiline = [
    "  __  __         _               ___                              _ ",
    " |  \\/  |___ _ _| |_ __ _ _ _   / __|___ _ __  _ __  __ _ _ _  __| |",
    " | |\\/| / _ \\ '_|  _/ _` | '_| | (__/ _ \\ '  \\| '  \\/ _` | ' \\/ _` |",
    " |_|  |_\\___/_|  \\__\\__,_|_|    \\___\\___/_|_|_|_|_|_\\__,_|_||_\\__,_|",
]


CREDITS_NAMES = "Perry Franks"
CREDITS = "By " + CREDITS_NAMES

welcome_messages = [
    "I'm the last one left.",
    "Welcome to hell.",
    "The major's dead.",
    "How will I protect these civilians.",
    "So many mouths to feed.",
    "I've never seen a sky like that.",
    "It's just me.",
    "Radio's dead. Commander's dead. We're Dead.",
    "This is Platoon Echo Zebra Niner - come in HQ... please god.",
    "I need to help these people.",
    "I need help.",
    "We've failed.",
    "There's no hope.",
    "Goddamn this war.",
    "What's the point in winning a war if everyone's dead.",
    "My gun's jammed with mud.",
]


def get_welcome_message() -> str:
    """
    Get a randomised welcome message. Messages are taken from the welcome_messages array.
    The length is not hard coded.
    :return: welcome message as a plaintext string
    """
    index = random.randint(0, len(welcome_messages) - 1)
    return welcome_messages[index]
