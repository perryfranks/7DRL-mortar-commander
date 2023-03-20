import copy

from engine import Engine
from factories.actor_factory import player
from game_world import GameWorld


def test_generate_floor():
    commander = copy.deepcopy(player)
    engine: Engine = Engine(player=commander)
    map_width: int = 5
    map_height: int = 5
    max_rooms: int = 5
    room_min_size: int = 5
    room_max_size: int = 5
    current_floor: int = 0

    g_world = GameWorld(
        engine=engine,
        map_width=map_width,
        map_height=map_height,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        current_floor=current_floor,
    )
    g_world.generate_floor()

    assert g_world.current_floor is 1
