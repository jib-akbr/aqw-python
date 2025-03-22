from bot.darkon_mats.core_darkon_mats import sukis_prestige
from core.bot import Bot
from core.commands import Command

async def main(cmd: Command):

    await sukis_prestige(cmd, 300)