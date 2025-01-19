from bot.darkon_mats.core_darkon_mats import ancient_remnant
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await ancient_remnant(cmd, 300)