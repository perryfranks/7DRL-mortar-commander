import pytest

import graphics
from actions import ItemAction
from components import consumable
from components.ai import DudAi
from components.consumable import Supplies
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item

supplies_value = 4


class DeadItemAction(ItemAction):
    pass


@pytest.fixture
def supplies():
    s = Supplies(4)
    return s


@pytest.fixture
def fully_kitted_entity() -> Actor:
    entity = Actor(
        char="o",
        color=(63, 127, 63),
        name="Test actor",
        ai_cls=DudAi,
        equipment=Equipment(),
        fighter=Fighter(hp=10, base_defense=0, base_power=0),
        inventory=Inventory(capacity=1),
        level=Level(level_up_factor=200),
    )
    return entity


@pytest.fixture
def kitted_w_supplies(fully_kitted_entity) -> Actor:
    supplies_item = Item(
        char="!",
        name="Supplies",
        consumable=consumable.Supplies(),
    )
    fully_kitted_entity.inventory.items.append(supplies_item)
    return fully_kitted_entity


def test_is_supplies(supplies):
    assert supplies.is_supplies is True


def test_supplies_activate(fully_kitted_entity, supplies):
    supplies_item = Item(
        char="!",
        name="Supplies",
        consumable=consumable.Supplies(),
    )

    dead_action = DeadItemAction(entity=fully_kitted_entity, item=supplies_item)
    supplies.activate(dead_action)


def test_consumable_consume(kitted_w_supplies):
    kitted_w_supplies.inventory.items[0].consumable.consume()
