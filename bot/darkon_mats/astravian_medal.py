from bot.darkon_mats.core_darkon_mats import astravian_medal
from core.bot import Bot
from core.command import Command

async def main(cmd: Command):

    await astravian_medal(cmd, 300)