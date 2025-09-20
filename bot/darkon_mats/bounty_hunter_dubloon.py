from bot.darkon_mats.core_darkon_mats import bounty_hunter_dubloon
from core.bot import Bot
from core.command import Command

async def main(cmd: Command):

    await bounty_hunter_dubloon(cmd, 300)