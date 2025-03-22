from bot.darkon_mats.core_darkon_mats import a_melody
from core.bot import Bot
from core.commands import Command

async def main(cmd: Command):
    await a_melody(cmd, 300)