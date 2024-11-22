from core.bot import Bot
from abstracts.command import Command

class JumpCmd(Command):
    
    def __init__(self, cell: str, pad: str):
        self.cell = cell
        self.pad = pad
    
    def execute(self, bot: Bot):
        bot.jump_cell(self.cell, self.pad)
        
    def to_string(self):
        return f"Jump : {self.cell} {self.pad}"