import components.consumables_mortars
import components.consumables_shells
import graphics.our_colors
from components import consumable
from entity import Item

supplies = Item(
    char="!",
    color=graphics.our_colors.supplies,
    name="Supplies",
    consumable=consumable.Supplies(),
)
basic_mortar = Item(
    char="|",
    color=graphics.our_colors.supplies,
    name="Basic Mortar",
    equippable=components.consumables_mortars.BasicMortar(
        range_increments=[
            (0, 5),
            (2, 2),
            (4, 1),
        ]
    )
)
basic_mortar_shell = Item(
    char="S",
    color=graphics.our_colors.supplies,
    name="Basic Shell",
    consumable=components.consumables_shells.BasicMortarShell(
        damage=3,
        radius=1,
    )
)
