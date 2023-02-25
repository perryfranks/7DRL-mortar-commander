from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_components import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item


class Equippable(BaseComponent):
    parent: Item

    def __init__(
            self,
            equipment_types: EquipmentType,
            power_bonus: int = 0,
            defense_bonus: int = 0,
    ):
        self.equipment_type = equipment_types
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus


class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_types=EquipmentType.WEAPON, power_bonus=2)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_types=EquipmentType.WEAPON, power_bonus=4)


class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_types=EquipmentType.WEAPON, power_bonus=4)


class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_types=EquipmentType.ARMOR, power_bonus=4)


class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_types=EquipmentType.ARMOR, power_bonus=4)
