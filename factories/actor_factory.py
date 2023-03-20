from components.ai import EnemySupplyScavenger
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Commander, Actor

player = Commander(
    char="X",
    color=(255, 255, 255),
    name="Player",
    ai_cls=EnemySupplyScavenger,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
)
scav = Actor(
    char="o",
    color=(63, 127, 63),
    name="Scavenger",
    ai_cls=EnemySupplyScavenger,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35),
)
