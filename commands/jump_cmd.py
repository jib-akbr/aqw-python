from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand

class JumpCmd(BaseCommand):
    
    def __init__(self, cell: str, pad: str):
        self.cell = cell
        self.pad = pad
    
    async def execute(self, bot: Bot, cmd: Command):
        if bot.player.CELL.lower() != self.cell or bot.player.PAD.lower() != self.pad:
            bot.jump_cell(self.cell, self.pad)
        
    def to_string(self):
        return f"Jump : {self.cell} {self.pad}"