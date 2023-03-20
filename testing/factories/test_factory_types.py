import copy

from factories.actor_factory import player


def test_player_commander_type():
    test_object = copy.deepcopy(player)
    assert isinstance(test_object, Commander)