from typing import Optional

import tcod.event
from actions import Action, EscapeAction, BumpAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_UP or key == tcod.event.K_k:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN or key == tcod.event.K_j:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT or key == tcod.event.K_h:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT or key == tcod.event.K_l:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # no valid key
        return action
