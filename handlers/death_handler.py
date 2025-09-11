import asyncio
from colorama import Fore

async def death_handler_task(bot: 'Bot'):
    print("Running death handler...")
    for i in range(11):
        await asyncio.sleep(1)
    bot.debug(Fore.MAGENTA + "respawned" + Fore.WHITE)
    bot.write_message(f"%xt%zm%resPlayerTimed%{bot.areaId}%{bot.user_id}%")
    bot.jump_cell(bot.player.CELL, bot.player.PAD)
    bot.player.ISDEAD = False
    print("Stopping death handler...")
    print("Spawned at cell:", bot.player.CELL, "pad:", bot.player.PAD)