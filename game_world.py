from engine import Engine
from procgen import generate_dungeon


class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """

    def __init__(
            self,
            *,
            engine: Engine,
            map_width: int,
            map_height: int,
            max_rooms: int,
            room_min_size: int,
            room_max_size: int,
            current_floor: int = 0
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = max_rooms

        self.room_min_size = room_min_size
        self.room_max_size = room_max_size

        self.current_floor = current_floor

    def generate_floor(self) -> None:
        """
        Generate a new dungeon and assign it to the current game map,
        this will overwrite the old dungeon immediately
        :return: None, as the output is already assigned to the engine's game map
        """
        self.current_floor += 1

        self.engine.game_map = generate_dungeon(
            max_rooms=self.max_rooms,
            room_min_size=self.room_min_size,
            room_max_size=self.room_max_size,
            map_width=self.map_width,
            map_height=self.map_height,
            engine=self.engine,
            friendly_spawn_rooms=3,
            enemy_spawn_rooms=3,
        )
