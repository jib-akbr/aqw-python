from core.bot import Bot
from abstracts.command import Command

class WalkCmd(Command):
    
    def __init__(self, x: str, y: str, speed: int = 8):
        self.x = x
        self.y = y
        self.speed = speed
    
    async def execute(self, bot: Bot):
        bot.walk_to(self.x, self.y, self.speed)
        
    def to_string(self):
        return f"Walk : {self.x} {self.y}"