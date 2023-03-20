from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import components.inventory
# from input_handlers import (
#    ActionOrHandler,
#    SingleRangedAttackHandler,
#    AreaRangedAttackHandler
# )
# import components.ai
from components.base_components import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item
    from input_handlers import ActionOrHandler


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class Supplies(Consumable):
    """
    The supply_item that everyone is trying to capture
    For now it just has a is supply_item func because I'm lazy
    """

    def __init__(self, value: int = 1):
        self.value = value

    def activate(self, action: actions.ItemAction) -> None:
        pass

    @property
    def is_supplies(self):
        return True


