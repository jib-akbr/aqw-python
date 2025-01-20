from bot.darkon_mats.core_darkon_mats import las_gratitude
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await las_gratitude(cmd, 300)