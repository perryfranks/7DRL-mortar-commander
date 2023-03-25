from typing import Tuple

import pytest

from components.ai import EnemySupplyScavenger
from components.consumables_mortars import BasicMortar
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Item, Commander, Entity, Actor

range_increments = [
    (0, 5),
    (2, 2),
    (4, 1),
]


@pytest.fixture
def basic_mortar() -> BasicMortar:
    return BasicMortar(
        range_increments=range_increments
    )


@pytest.fixture
def mortar_item(basic_mortar) -> Item:
    basic_mortar = Item(
        char="|",
        name="Basic Mortar",
        equippable=basic_mortar
    )
    return basic_mortar


@pytest.fixture
def entity_w_mortar(mortar_item) -> Commander:
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
    player.inventory.items.append(mortar_item)
    return player


def update_pos(entity: Actor) -> Tuple[int, int]:
    entity.inventory.items[0].x = 4
    entity.inventory.items[0].y = 4


def test_shot_count_setter(basic_mortar):
    assert basic_mortar.shot_count == 0
    basic_mortar.shot_count = -4
    assert basic_mortar.shot_count == 0
    basic_mortar.shot_count = 4
    assert basic_mortar.shot_count == 4
    basic_mortar.shot_count = -13
    assert basic_mortar.shot_count == 0


def test_prev_xy(entity_w_mortar):
    # Entity is given a default placement of 0,0
    mortar = entity_w_mortar.get_mortar()
    assert mortar.prev_xy[0] == 0
    assert mortar.prev_xy[1] == 0
    update_pos(entity_w_mortar)
    assert mortar.prev_xy[0] == 0
    assert mortar.prev_xy[1] == 0
    mortar.update_xy()
    assert mortar.prev_xy[0] == 4
    assert mortar.prev_xy[1] == 4


def test_has_moved(entity_w_mortar):
    assert entity_w_mortar.get_mortar().has_moved is False
    entity_w_mortar.inventory.items[0].x = 4
    entity_w_mortar.inventory.items[0].y = 4
    assert entity_w_mortar.get_mortar().has_moved is True


def test_get_range(basic_mortar):
    # no shoots
    assert basic_mortar.get_range == 5
    basic_mortar.shot_count = 2
    assert basic_mortar.get_range == 2
    basic_mortar.shot_count = 3
    assert basic_mortar.get_range == 2
    basic_mortar.shot_count = 4
    assert basic_mortar.get_range == 1
    basic_mortar.shot_count = 5
    assert basic_mortar.get_range == 1
    # stupidly high
    basic_mortar.shot_count = 100
    assert basic_mortar.get_range == 1
    # we don't want it to loop to the other end of the array
    basic_mortar.shot_count = -1
    assert basic_mortar.get_range == 5


def test_shoot_no_move(entity_w_mortar):
    mortar = entity_w_mortar.get_mortar()
    assert mortar.shoot() == 5
    assert mortar.shot_count == 1
    mortar.shot_count = 4
    assert mortar.shoot() == 1
    assert mortar.shot_count == 5


def test_shoot_move(entity_w_mortar):
    mortar = entity_w_mortar.get_mortar()
    update_pos(entity_w_mortar)
    assert mortar.has_moved is True
    assert mortar.shoot() == 5
    assert mortar.shot_count == 1


def test_under_fire():
    assert False
