from bot.darkon_mats.core_darkon_mats import bandits_correspondence
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await bandits_correspondence(cmd, 3000)