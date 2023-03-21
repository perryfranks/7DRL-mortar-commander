import pytest

from components.equipment import Equipment
from components.equipment_types import EquipmentType
from components.equippable import Equippable
from components.equippable_fantasy import Dagger, LeatherArmor
from entity import Item

weapon = Item(
    char="/",
    color=(0, 191, 255),
    name="Dagger",
    equippable=Dagger()
)
custom_weapon = Item(
    char="/",
    color=(0, 191, 255),
    name="Custom Dagger",
    equippable=Equippable(
        equipment_type=EquipmentType.WEAPON,
        defense_bonus=1,
        power_bonus=1,
    )
)

armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=LeatherArmor(),
)
custom_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Custom Leather Armor",
    equippable=Equippable(
        equipment_type=EquipmentType.ARMOR,
        defense_bonus=2,
        power_bonus=2,
    ),
)


@pytest.fixture
def equipment() -> Equipment:
    """
    Create an equipment object variables based of the global variables above.
    The equipment will have a weapon and an armor quality
    """

    equipment = Equipment(weapon, armor)
    return equipment


def test_equipment_constructor_no_args():
    test_obj = Equipment()
    assert test_obj.armor is None
    assert test_obj.weapon is None


def test_defense_bonus_empty():
    equipment = Equipment()
    assert equipment.defense_bonus == 0


def test_defense_bonus(equipment):
    # Dagger + leather armor is only 1 damage bonus
    assert equipment.defense_bonus == 1


def test_defense_bonus_double_defense(equipment):
    equipment.weapon = custom_weapon
    assert equipment.defense_bonus == 2


def test_power_bonus_empty():
    equipment = Equipment()
    assert equipment.power_bonus == 0


def test_power_bonus(equipment):
    expected_power_bonus = weapon.equippable.power_bonus
    assert equipment.power_bonus == expected_power_bonus


def test_power_bonus_double_attack(equipment):
    equipment.armor = custom_armor
    expected_power_bonus = weapon.equippable.power_bonus + custom_armor.equippable.power_bonus
    assert equipment.power_bonus == expected_power_bonus


def test_item_is_equipped_armor():
    equipment = Equipment(armor=armor)
    assert equipment.item_is_equipped(armor) is True
    assert equipment.item_is_equipped(custom_armor) is False


def test_item_is_equipped_weapon():
    equipment = Equipment(weapon=weapon)
    assert equipment.item_is_equipped(weapon) is True
    assert equipment.item_is_equipped(custom_armor) is False


def test_item_is_equipped_both():
    equipment = Equipment(weapon=weapon, armor=armor)
    assert equipment.item_is_equipped(weapon) is True
    assert equipment.item_is_equipped(armor) is True


def test_equip_to_slot(equipment):
    assert equipment.weapon == weapon
    assert equipment.armor == armor
    equipment.equip_to_slot("weapon", custom_weapon, False)
    equipment.equip_to_slot("armor", custom_armor, False)
    assert equipment.weapon == custom_weapon
    assert equipment.armor == custom_armor


def test_equip_to_slot_wrong_text(equipment):
    equipment.equip_to_slot("wrong", custom_weapon, False)
    assert equipment.armor is not None
    assert equipment.weapon is not None


def test_unequip_from_slot_weapon(equipment):
    assert equipment.weapon is not None
    equipment.unequip_from_slot("weapon", False)  # Message is false since I don't know how to mock
    assert equipment.weapon is None


def test_unequip_from_slot_armor(equipment):
    assert equipment.armor is not None
    equipment.unequip_from_slot("armor", False)  # Message is false since I don't know how to mock
    assert equipment.armor is None


def test_unequip_from_slot_wrong_attr(equipment):
    equipment.unequip_from_slot("wrong", False)  # Message is false since I don't know how to mock
    assert equipment.armor is not None
    assert equipment.weapon is not None


def test_toggle_equip_equipped_gear(equipment):
    equipment.toggle_equip(weapon, False)
    equipment.toggle_equip(armor, False)
    assert equipment.weapon is None
    assert equipment.armor is None


def test_toggle_equip_unequipped_gear(equipment):
    equipment.unequip_from_slot("weapon", False)
    equipment.unequip_from_slot("armor", False)
    equipment.toggle_equip(weapon, False)
    equipment.toggle_equip(armor, False)
    assert equipment.weapon == weapon
    assert equipment.armor == armor
