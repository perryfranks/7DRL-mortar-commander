from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING

import entity_factories

if TYPE_CHECKING:
    from entity import Entity

max_items_by_floor = [
    (1, 25),
    (4, 35),
]

max_monsters_by_floor = [
    (1, 36),
    (4, 10),
    (6, 20),
]

item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.supplies, 35)],
    2: [(entity_factories.supplies, 10)],
    4: [(entity_factories.supplies, 25), (entity_factories.supplies, 5)],
    6: [(entity_factories.supplies, 25), (entity_factories.supplies, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 80)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}
