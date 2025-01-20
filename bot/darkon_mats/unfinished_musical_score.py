from bot.darkon_mats.core_darkon_mats import unfinished_musical_score
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await unfinished_musical_score(cmd, 300)