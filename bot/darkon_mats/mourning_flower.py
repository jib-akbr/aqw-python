from bot.darkon_mats.core_darkon_mats import mourning_flower
from core.bot import Bot
from core.command import Command

async def main(cmd: Command):

    await mourning_flower(cmd, 1000)