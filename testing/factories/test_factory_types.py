import copy

from typing import TYPE_CHECKING
from factories.actor_factory import player

if TYPE_CHECKING:
    from entity import Commander


def test_player_commander_type():
    test_object = copy.deepcopy(player)
    assert isinstance(test_object, Commander)