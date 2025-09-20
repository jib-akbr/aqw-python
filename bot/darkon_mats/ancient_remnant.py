from bot.darkon_mats.core_darkon_mats import ancient_remnant
from core.bot import Bot
from core.command import Command

async def main(cmd: Command):

    await ancient_remnant(cmd, 300)