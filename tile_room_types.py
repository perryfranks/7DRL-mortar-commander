from enum import Enum, auto
from typing import Tuple

import numpy as np  # type: ignore

import graphics.generic_colors
import graphics.generic_colors as gc

# Tile graphics structured type compatible with Console.tiles_rgb
# whatever that means
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        # looks like np.bool has been depreciated which sucks
        ("walkable", bool),  # True if this tile can be walked over.
        ("transparent", bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
        *,  # enforce the use of keywords, so that parameter  order doesn't matter.
        walkable: int,
        transparent: int,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50)),
)
spawn_floor_enemy = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), gc.dark_red),
    light=(ord(" "), (255, 255, 255), gc.dark_red),
)
spawn_floor_friendly = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), gc.dark_green),
    light=(ord(" "), (255, 255, 255), gc.dark_green),
)
# wall = new_tile(
#     walkable=False,
#     transparent=True,
#     dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
#     light=(ord(" "), (255, 255, 255), (130, 110, 50)),
# )
wall = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), graphics.generic_colors.indigo),
    light=(ord(" "), (255, 255, 255), graphics.generic_colors.indigo),
)
down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(">"), (0, 0, 100), (50, 50, 150)),
    light=(ord(">"), (255, 255, 255), (200, 180, 50)),
)


class RoomTypes(Enum):
    REGULAR = auto()
    ENEMY_SPAWN = auto()
    FRIENDY_SPAWN = auto()
