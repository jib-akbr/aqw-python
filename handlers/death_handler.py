import asyncio
from datetime import datetime
from colorama import Fore

async def death_handler_task(bot: 'Bot'):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Running death handler...")
    for i in range(11):
        await asyncio.sleep(1)
    bot.debug(Fore.MAGENTA + "respawned" + Fore.WHITE)
    bot.write_message(f"%xt%zm%resPlayerTimed%{bot.areaId}%{bot.user_id}%")
    bot.jump_cell("Enter", "Left")
    bot.player.ISDEAD = False
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Stopping death handler...")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Spawned at cell:", bot.player.CELL, "pad:", bot.player.PAD)