import asyncio
from colorama import Fore

async def death_handler_task(bot: 'Bot'):
    print("Running death handler...")
    await asyncio.sleep(11)
    bot.debug(Fore.MAGENTA + "respawned" + Fore.WHITE)
    bot.write_message(f"%xt%zm%resPlayerTimed%{bot.areaId}%{bot.user_id}%")
    bot.jump_cell(bot.player.CELL, bot.player.PAD)
    bot.player.ISDEAD = False
    print("Stopping death handler...")