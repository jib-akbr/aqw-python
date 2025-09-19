import asyncio
from typing import List, Union, Callable, Any, Optional, TYPE_CHECKING
import time
from functools import wraps
from inspect import iscoroutinefunction
from datetime import datetime, timedelta
from colorama import Fore
from model.inventory import ItemType, ItemInventory, ScrollType
from model.shop import Shop
from model import Monster, PlayerArea
import json
from core.utils import normalize

if TYPE_CHECKING:
    from core.bot import Bot


class _CommandBase:
    """Shared attributes across command mixins."""
    bot: "Bot"


def check_alive(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def sync_wrapper(self, *args: Any, **kwargs: Any) -> Any:
        if self.is_player_alive():
            return func(self, *args, **kwargs)
        start_time = time.time()
        timeout = 11  # Maximum time to wait (in seconds)
        count = 1
        while self.is_still_connected():
            if self.is_player_alive():
                return func(self, *args, **kwargs)
            if time.time() - start_time > timeout:
                print("timeout from @check_alive sync")
                self.bot.debug(Fore.MAGENTA + "respawned: from @check_alive sync" + Fore.WHITE)
                self.bot.write_message(f"%xt%zm%resPlayerTimed%{self.bot.areaId}%{self.bot.user_id}%")
                self.bot.jump_cell(self.bot.player.CELL, self.bot.player.PAD)
                self.bot.player.ISDEAD = False
                print("Spawned at cell:", self.bot.player.CELL, "pad:", self.bot.player.PAD)
                # self.stopBot("from @check_alive sync")
                return func(self, *args, **kwargs)
            time.sleep(1)  # Avoid busy-waiting
            count += 1
        if not self.is_still_connected():
            print("STOPPPPPPPP SYNC")
            return
        self.bot.debug(Fore.MAGENTA + "respawned: from @check_alive sync" + Fore.WHITE)
        self.bot.write_message(f"%xt%zm%resPlayerTimed%{self.bot.areaId}%{self.bot.user_id}%")
        self.bot.jump_cell(self.bot.player.CELL, self.bot.player.PAD)
        self.bot.player.ISDEAD = False
        print("Spawned at cell:", self.bot.player.CELL, "pad:", self.bot.player.PAD)
        return func(self, *args, **kwargs)

    @wraps(func)
    async def async_wrapper(self, *args: Any, **kwargs: Any) -> Any:
        if self.is_player_alive():
            return await func(self, *args, **kwargs)
        start_time = time.time()
        timeout = 11  # Maximum time to wait (in seconds)

        while self.is_still_connected():
            if self.is_player_alive():
                return await func(self, *args, **kwargs)
            if time.time() - start_time > timeout:
                print("timeout from @check_alive async")
                self.bot.debug(Fore.MAGENTA + "respawned: from @check_alive sync" + Fore.WHITE)
                self.bot.write_message(f"%xt%zm%resPlayerTimed%{self.bot.areaId}%{self.bot.user_id}%")
                self.bot.jump_cell(self.bot.player.CELL, self.bot.player.PAD)
                self.bot.player.ISDEAD = False
                print("Spawned at cell:", self.bot.player.CELL, "pad:", self.bot.player.PAD)
                # self.stopBot("from @check_alive async")
                return await func(self, *args, **kwargs)
            await asyncio.sleep(1)  # Non-blocking wait
        if not self.is_still_connected():
            print("STOPPPPPPPP ASYNC")
            return
        self.bot.debug(Fore.MAGENTA + "respawned: from @check_alive async" + Fore.WHITE)
        self.bot.write_message(f"%xt%zm%resPlayerTimed%{self.bot.areaId}%{self.bot.user_id}%")
        self.bot.jump_cell(self.bot.player.CELL, self.bot.player.PAD)
        self.bot.player.ISDEAD = False
        print("Spawned at cell:", self.bot.player.CELL, "pad:", self.bot.player.PAD)
        return await func(self, *args, **kwargs)
    # Check if the function is async and use the appropriate wrapper
    return async_wrapper if iscoroutinefunction(func) else sync_wrapper
