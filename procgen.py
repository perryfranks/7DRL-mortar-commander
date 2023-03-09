from __future__ import annotations

import random
from typing import Dict, Iterator, List, Tuple, TYPE_CHECKING, Optional

import tcod

import exceptions
import tile_room_types
from game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
# from procgen.weights import max_monsters_by_floor, max_items_by_floor, enemy_chances, item_chances
import weights


def get_max_value_for_floor(
        max_value_by_floor: List[Tuple[int, int]], floor: int
) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
        weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
        number_of_entities: int,
        floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(
        entities, weights=entity_weighted_chance_values, k=number_of_entities
    )

    return chosen_entities


class RectangularRoom:
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            type: tile_room_types.RoomTypes = tile_room_types.RoomTypes.REGULAR
    ):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.type = type

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int, ) -> None:
    # todo: remove monsters
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(weights.max_monsters_by_floor, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(weights.max_items_by_floor, floor_number)
    )

    monsters: List[Entity] = get_entities_at_random(
        weights.enemy_chances, number_of_monsters, floor_number
    )
    items: List[Entity] = get_entities_at_random(
        weights.item_chances, number_of_items, floor_number
    )

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
        friendly_spawn_rooms: int = 0,
        enemy_spawn_rooms: int = 0,
        padding_total_ratio: int = 5,
) -> GameMap:
    """
    Generate the dungeon and return as a GameMap object. By not providing any spawn room counts the old rogue tutorial
    style dungeon will be created.
    :param max_rooms:
    :param room_min_size:
    :param room_max_size:
    :param map_width:
    :param map_height:
    :param engine:
    :param friendly_spawn_rooms: number of friendly spawn rooms to have     
    :param enemy_spawn_rooms:
    :param padding_total_ratio: NOT IMPLEMENTED the ratio of the map height that should be for spawn rooms.
            Will be divided between top and bottom
    :return:
    """
    # if we don't have spawn rooms specified default to the old, generation method
    if friendly_spawn_rooms == enemy_spawn_rooms == 0:
        return default_generation(
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            map_width=map_width,
            map_height=map_height,
            engine=engine
        )

    # light lanes - have the spawn rooms creating some lanes and leave the rest of the generation faily unchanged
    # Heavy lanes - split the map into slices depending on the number of spawns and contain paths to their own lanes

    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    # The padding to provide to the top and bottom on the screen. I think 1/8 between them is fair
    padding = map_height // 6
    # for now lets duplicate
    enemy_spawn_interval = map_width // enemy_spawn_rooms

    dungeon = padded_generation(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine,
        padding_total=map_height // 2
    )

    # for i in range(enemy_spawn_rooms):
    quarter_interval = enemy_spawn_interval // 4
    y = 1
    height = padding - 2
    width = enemy_spawn_interval // 2
    for i in range(enemy_spawn_rooms):
        # create the spawn room
        midpoint = enemy_spawn_interval // 2 + (i * enemy_spawn_interval)  # also width +
        x = midpoint - quarter_interval
        spawn_room = RectangularRoom(
            x=x,
            y=y,
            width=width,
            height=height,
            type=tile_room_types.RoomTypes.ENEMY_SPAWN
        )
        dungeon.tiles[spawn_room.inner] = tile_room_types.spawn_floor_enemy
        # Connect it to the main land
        dungeon = connect_spawn(spawn_room, dungeon, True, 2)

    friendly_interval = map_width // friendly_spawn_rooms
    quarter_interval = friendly_interval // 4
    y = map_height - padding
    width = friendly_interval // 2
    for i in range(friendly_spawn_rooms):
        # create the spawn room
        midpoint = friendly_interval // 2 + (i * friendly_interval)
        x = midpoint - quarter_interval
        spawn_room = RectangularRoom(
            x=x,
            y=y,
            width=width,
            height=height,
            type=tile_room_types.RoomTypes.FRIENDY_SPAWN
        )
        dungeon.tiles[spawn_room.inner] = tile_room_types.spawn_floor_friendly
        dungeon = connect_spawn(spawn_room, dungeon, False, 2)

    return dungeon


def connect_spawn(room: RectangularRoom, dungeon: GameMap, is_enemy: bool, tunnel_ratio: int) -> Optional[GameMap]:
    """
    Connect a spawn room with the rest of the dungeon.
    If is_enemy is true then the movement is down for making a tunnel
    :param tunnel_ratio: as a ratio the length of the dungeon to climb when looking for a tunnel. Cannot equal 0
    :return: Will return the modified map
    """
    if tunnel_ratio == 0:
        return None

    start = (room.center[0], room.y2)
    # range doesn't like a range like range(9,1) so we need to normalise first
    height_ratio = dungeon.height // tunnel_ratio
    width_ratio = dungeon.width // tunnel_ratio
    if not is_enemy:
        start = (room.center[0], room.y1)
        interval = range(height_ratio, start[1])
        interval = reversed(interval)
    else:
        interval = range(start[1], height_ratio)
    last = 0
    for i in interval:
        last = i
        if dungeon.tiles[start[0], i] == tile_room_types.floor:
            # we have found our needed location so dig here
            return tunnel(start, (start[0], i), dungeon)  # hopefully this works backwards

    dungeon = tunnel(start, (start[0], last), dungeon)
    # now do this process horizontal
    # if on left half move right. Opposite left
    # new_start = (start[0], last)
    new_start = (start[0] + 1, last)
    if new_start[0] < (width_ratio):
        interval = range(new_start[0], new_start[0] + width_ratio)
    else:
        interval = range(new_start[0] + width_ratio, new_start[0] - 1, -1)
        # interval = range(new_start[0] + dungeon.width // 2, new_start[0] - 1)
        # interval = reversed(interval)

    # FIXME: there is some strange bug here
    # FIXME: index 106 is out of bounds for axis 0 with size 80
    # FIXME: add cases for getting to the edge
    #
    for i in interval:
        # Be lazy and just check if we're out of bounds
        if i >= dungeon.width or i < 0:
            continue
        if dungeon.tiles[i, new_start[1]] == tile_room_types.floor:
            return tunnel(new_start, (i, new_start[1]), dungeon)

    print("No room was found. Giving up is not the best play")
    print("What we should do is regen the dungeon")
    return dungeon


def tunnel(
        point1: Tuple[int, int], point2: Tuple[int, int], d: GameMap
) -> GameMap:
    for x, y in tunnel_between(point1, point2):
        d.tiles[x, y] = tile_room_types.floor
    return d


def make_room(
        x: int,
        y: int,
        room_width: int,
        room_height: int,
        type: tile_room_types.RoomTypes = tile_room_types.RoomTypes.REGULAR
) -> RectangularRoom:
    """
    Handle making a room.
    Incredibly simple for now. May need more logic later and reduces duplication.
    """
    return RectangularRoom(x=x, y=y, width=room_width, height=room_height, type=type)


def padded_generation(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
        padding_total: int
) -> GameMap:
    """
    Generate a new dungeon map with padding at the top and bottom equal to padding_total / 2.
    Does not place the player.
    """
    if padding_total == 0:
        raise exceptions.Impossible("Padding size of given was given to padded_generation while building dungeon.")

    dungeon = GameMap(engine, map_width, map_height, entities=[])

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0 + padding_total // 2, dungeon.height - room_height - 1 - padding_total // 2)

        new_room = make_room(x, y, room_width, room_height, tile_room_types.RoomTypes.REGULAR)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        dungeon.tiles[new_room.inner] = tile_room_types.floor

        # if len(rooms) == 0:
        #     # The first room, where the player starts.
        #     player.place(*neNw_room.center, dungeon)
        # else:  # All rooms after the first.
        #     # Dig out a tunnel between this room and the previous one.
        #     for x, y in tunnel_between(rooms[-1].center, new_room.center):
        #         dungeon.tiles[x, y] = tile_room_types.floor

        if len(rooms) > 0:
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_room_types.floor

        place_player_center(engine, dungeon)
        place_entities(new_room, dungeon, engine.game_world.current_floor)

        # Can add stairs here if needed. Will be added to final room
        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon


def default_generation(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    print("default gen ran")
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = make_room(x, y, room_width, room_height)
        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_room_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            tunnel(rooms[-1].center, new_room.center, dungeon)
            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_room_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon


def place_player_center(engine: Engine, dungeon: GameMap) -> None:
    player = engine.player
    dungeon.entities.add(player)
    player.place(
        dungeon.width // 2,
        dungeon.height // 2,
        dungeon
    )
