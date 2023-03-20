import components.equippable_fantasy
from entity import Item

dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=components.equippable_fantasy.Dagger()
)
sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=components.equippable_fantasy.Sword())
leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=components.equippable_fantasy.LeatherArmor(),
)
chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=components.equippable_fantasy.ChainMail()
)
