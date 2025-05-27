from core.bot import Bot
from core.commands import Command
from bot.LR.core_lr import exalted_crown

async def main(cmd: Command):
    await exalted_crown(cmd)