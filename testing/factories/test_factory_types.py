import copy
from typing import TYPE_CHECKING

from components.consumable import Supplies
from factories.actor_factory import player, scav
from entity import Commander, Actor
from factories.item_factory import supplies


def test_player_commander_type():
    test_object = copy.deepcopy(player)
    assert isinstance(test_object, Commander)


def test_scav_type():
    test_object = copy.deepcopy(scav)
    assert isinstance(test_object, Actor)
