import pytest

from components.ai import EnemySupplyScavenger
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Commander


@pytest.fixture
def level():
    l = Level()
    return l


@pytest.fixture
def entity_w_mortar() -> Commander:
    player = Commander(
        char="X",
        color=(255, 255, 255),
        name="Player",
        ai_cls=EnemySupplyScavenger,
        equipment=Equipment(),
        fighter=Fighter(hp=30, base_defense=1, base_power=2),
        inventory=Inventory(capacity=26),
        level=Level(level_up_base=200),
    )
    return player


def test_experience_to_next_level(level):
    assert level.experience_to_next_level == 150
    level.add_xp(1)
    assert level.experience_to_next_level == 149


def test_requires_level_up(level):
    assert level.requires_level_up is False
    level.current_level = 165
    print(level.experience_to_next_level )
    assert level.requires_level_up is True

def test_add_xp():
    assert False


def test_increase_level(level):
    assert level.current_level == 1
    level.increase_level()
    assert level.current_level == 2


def test_increase_max_hp():
    assert False


def test_increase_power():
    assert False


def test_increase_defense():
    assert False
