from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import helper
from components.equippable import Equippable
from equipment_types import EquipmentType
from game_map import GameMap

if TYPE_CHECKING:
    from entity import Item


class BasicMortar(Equippable):
    """
    Basic Mortar weapon that has additional attributes & functions for handling increasing accuracy.

        # can be expanded with:
        # move speed
        # accuracy changes
        # range
        # shot delay
    """
    parent: Item
    range_increments: List[Tuple[int, int]]
    prev_xy = Tuple[int, int]

    def __init__(self, range_increments: List[Tuple[int, int]]) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, power_bonus=2)
        # [count (accumulative), range]
        self.range_increments = range_increments
        self.shot_count = 0

    def second_init(self):
        self.prev_xy = self.parent.x, self.parent.y

    @property
    def has_moved(self) -> bool:
        return self.prev_xy[0] != self.parent.x or self.prev_xy[1] != self.parent.y

    @property
    def get_range(self) -> int:
        """
        Get the range based off the current shot_count. Does not check has_moved or increment the counter.
        For that use shoot().
        :return: int for the cardinal distance of the explosive
        """
        for i in self.range_increments:
            if self.shot_count <= i[0]:
                return i[1]
        # max range
        return self.range_increments[-1][1]

    def shoot(self) -> int:
        """
        'Shoot' by checking whether mortar has moved and reset the conditions if so. Will return the range distance
        in line with the range_increments
        :return: int for the cardinal distance of the explosive
        """
        print("basic mortar item.shoot() called")
        if self.has_moved:
            self.shot_count = 1  # Reset and then increment
        else:
            self.shot_count += 1
        return self.get_range

    def under_fire(self, x: int, y: int, game_map: GameMap) -> List[Tuple[int, int]]:
        """
        TODO: I think this is not nice coupling
        Given a xy position then get the list of affected indexes.
        Does not work off entities within the range. So can be
        used for highlighting all tiles in the area
        """
        under_fire = []
        for map_x in range(game_map.width):
            for map_y in range(game_map.height):
                if helper.two_point_distance(xy1=(x, y), xy2=(map_x, map_y)) < self.get_range:
                    under_fire.append((map_x, map_y))
        return under_fire
