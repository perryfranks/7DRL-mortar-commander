from components.ai import EnemySupplyScavenger
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Actor

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=EnemySupplyScavenger,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100),
)
