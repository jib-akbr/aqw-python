from core.bot import Bot
from abstracts.command import Command
import time

class SleepCmd(Command):
    
    def __init__(self, milliseconds: int):
        self.milliseconds = milliseconds
    
    def execute(self, bot: Bot):
        bot.doSleep(self.milliseconds)
        
    def to_string(self):
        return f"Sleep {self.milliseconds}ms"