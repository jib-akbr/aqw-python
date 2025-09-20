import asyncio
from datetime import datetime
from typing import TYPE_CHECKING
from colorama import Fore

if TYPE_CHECKING:
    from core.bot import Bot
    
async def death_handler_task(bot: 'Bot'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running death handler...")
    for i in range(11):
        await asyncio.sleep(1)
    bot.debug(Fore.MAGENTA + "respawned" + Fore.WHITE)
    bot.write_message(f"%xt%zm%resPlayerTimed%{bot.areaId}%{bot.user_id}%")
    if bot.respawn_cell_pad:
        bot.jump_cell(bot.respawn_cell_pad[0], bot.respawn_cell_pad[1])
    else:
        bot.jump_cell(bot.player.CELL, bot.player.PAD)
    bot.player.ISDEAD = False
    bot.player.MANA = 100
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping death handler...")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Spawned at cell:", bot.player.CELL, "pad:", bot.player.PAD)