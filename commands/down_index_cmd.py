from core.bot import Bot
from abstracts.command import Command

class DownIndexCmd(Command):
    skip_delay = True
    
    def __init__(self, value: int):
        self.value = value
    
    def execute(self, bot: Bot):
        bot.index += self.value
        
    def to_string(self):
        # return f"Down Index : {self.value}"
        return None