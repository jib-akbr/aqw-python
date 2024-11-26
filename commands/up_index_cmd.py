from core.bot import Bot
from abstracts.command import Command

class UpIndexCmd(Command):
    skip_delay = True
    
    def __init__(self, value: int):
        self.value = value
    
    def execute(self, bot: Bot):
        bot.index -= self.value + 1
        
    def to_string(self):
        # return f"Up Index : {self.value}"
        return None