from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING

import factories.actor_factory
import factories.fantasy_entity_factory
import factories.item_factory

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
    0: [(factories.item_factory.supplies, 35)],
    2: [(factories.item_factory.supplies, 10)],
    4: [(factories.item_factory.supplies, 25), (factories.item_factory.supplies, 5)],
    6: [(factories.item_factory.supplies, 25), (factories.item_factory.supplies, 15)],
}

enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(factories.actor_factory.scav, 80)],
    3: [(factories.fantasy_entity_factory.troll, 15)],
    5: [(factories.fantasy_entity_factory.troll, 30)],
    7: [(factories.fantasy_entity_factory.troll, 60)],
}
