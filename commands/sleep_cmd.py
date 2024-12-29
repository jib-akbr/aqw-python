from core.bot import Bot
from abstracts.command import Command
import asyncio

class SleepCmd(Command):
    skip_delay = True
    
    def __init__(self, milliseconds: int):
        self.milliseconds = milliseconds
    
    async def execute(self, bot: Bot):
        await asyncio.sleep(self.milliseconds/1000)
        
    def to_string(self):
        return f"Sleep {self.milliseconds}ms"