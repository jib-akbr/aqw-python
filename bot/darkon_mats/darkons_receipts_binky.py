from bot.darkon_mats.core_darkon_mats import darkons_receipts_binky
from core.bot import Bot
from core.commands import Command

async def main(bot: Bot):
    cmd = Command(bot)

    await darkons_receipts_binky(cmd, 222)