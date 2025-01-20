from bot.darkon_mats.core_darkon_mats import astravian_medal
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await astravian_medal(cmd, 300)