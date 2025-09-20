from bot.darkon_mats.core_darkon_mats import darkons_receipts_binky
from core.bot import Bot
from core.command import Command

async def main(cmd: Command):

    await darkons_receipts_binky(cmd, 222)