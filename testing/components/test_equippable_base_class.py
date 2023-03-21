from components.equipment_types import EquipmentType
from components.equippable import Equippable


def test_equippable_default_args():
    test_obj = Equippable(EquipmentType.WEAPON)
    assert test_obj.power_bonus == 0
    assert test_obj.defense_bonus == 0
    assert test_obj.equipment_type == EquipmentType.WEAPON
    assert test_obj.equipment_type != EquipmentType.ARMOR


def test_equippable_constructor():
    power = 2
    defense = 6
    test_obj = Equippable(EquipmentType.WEAPON, power, defense)
    assert test_obj.power_bonus == power
    assert test_obj.defense_bonus == defense
    assert test_obj.equipment_type == EquipmentType.WEAPON
    assert test_obj.equipment_type != EquipmentType.ARMOR
