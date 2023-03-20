from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
from components.consumable import Consumable

if TYPE_CHECKING:
    from entity import Actor
    import input_handlers as ih


class BasicMortarShell(Consumable):
    """
    The damage part of the mortar. A lot of the stats will be given by the used mortar equipment
    """

    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> Optional[ih.ActionOrHandler]:
        return ih.MortarAreaAttackHandler(
            self.engine,
            radius=self.radius,  # this would be for displaying something
        )

    def activate(self, action: actions.ItemAction) -> None:
        target_xy = action.target_xy
        print("basic mortar shell fired")
        # unlike fireball we don't care if you can see something

        targets_hit = 0

        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) <= self.radius:
                self.engine.message_log.add_message(
                    f"A {actor.name} is sprayed with debris, shrapnel, and mud. {self.damage} damage."
                )
                actor.fighter.take_damage(self.damage)
                targets_hit += 1

        self.consume()
