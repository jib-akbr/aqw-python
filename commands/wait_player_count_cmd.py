from core.bot import Bot
from abstracts.command import Command

class WaitPlayerCountCmd(Command):
    
    def __init__(self, playerCount: int):
        self.playerCount = playerCount
    
    async def execute(self, bot: Bot):
        if len(bot.user_ids) < self.playerCount:
            bot.index -= 1
        
    def to_string(self):
        return f"Waiting for : [{self.playerCount}] player(s)"