import components.consumables_fantasy
from entity import Item

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=components.consumables_fantasy.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=components.consumables_fantasy.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=components.consumables_fantasy.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=components.consumables_fantasy.LightningDamageConsumable(damage=20, maximum_range=5),
)
