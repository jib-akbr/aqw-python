from core.bot import Bot
from abstracts.command import Command

class ToLabelCmd(Command):
    skip_delay = True
    
    def __init__(self, label: str):
        self.label = label.upper()
    
    async def execute(self, bot: Bot):
        for i, cmd in enumerate(bot.cmds):
            if cmd.to_string() == f"[{self.label}]":
                bot.index = i
        
    def to_string(self):
        return f"To label : [{self.label}]"