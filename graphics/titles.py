"""
Constant strings and functions related to the title screen, credits,
or other items that are mostly text strings mostly just printed to the user
"""
import random

TITLE = "Name"

CREDITS_NAMES = "Perry Franks"
CREDITS = "By " + CREDITS_NAMES

welcome_messages = [
    "Hello and welcome, adventurer, to yet another dungeon!",
    "Welcome to the depths",
    "Say friend and enter",
]


def get_welcome_message() -> str:
    index = random.randint(0, len(welcome_messages))
    return welcome_messages[index]
