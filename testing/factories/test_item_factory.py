import copy

from components.consumable import Supplies
from components.consumables_mortars import BasicMortar
from components.consumables_shells import BasicMortarShell
from entity import Item
from factories.item_factory import supplies, basic_mortar, basic_mortar_shell


def test_supplies_type():
    test_object = copy.deepcopy(supplies)
    assert isinstance(test_object, Item)
    assert test_object.consumable
    assert isinstance(test_object.consumable, Supplies)


def test_basic_mortar_type():
    test_object: Item = copy.deepcopy(basic_mortar)
    assert isinstance(test_object, Item)
    assert test_object.equippable
    assert isinstance(test_object.equippable, BasicMortar)

def test_basic_mortar_shell_type():
    test_object: Item = copy.deepcopy(basic_mortar_shell)
    assert isinstance(test_object, Item)
    assert test_object.consumable
    assert isinstance(test_object.consumable, BasicMortarShell)
