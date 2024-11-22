from core.bot import Bot
from abstracts.command import Command

class MessageCmd(Command):
    
    def __init__(self, msg: str):
        self.msg = msg
    
    def execute(self, bot: Bot):
        pass
        
    def to_string(self):
        return f"{self.msg}"