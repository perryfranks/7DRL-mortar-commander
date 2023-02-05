import random
from typing import Tuple, Iterator
from game_map import GameMap
import tile_types
import tcod
class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index"""
        return slice(self.x1 + 1 , self.x2), slice(self.y1 + 1, self.y2)


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int ]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # move hoz then vert
        corner_x, corner_x = x2, y1
    else:
        # Move vert then hoz
        corner_x, corner_x = x1, y2

    # Generate the coords for this tunnel
    HERE
def generate_dungeon(map_width, map_height) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    room_1 = RectangularRoom(x=20, y=15, width=10, height=15)
    room_2 = RectangularRoom(x=35, y=15, width=10, height=15)

    dungeon.tiles[room_1.inner] = tile_types.floor
    dungeon.tiles[room_2.inner] = tile_types.floor

    return dungeon
