from core.bot import Bot
from core.commands import Command
from abstracts.base_command import BaseCommand

class JoinHouseCmd(BaseCommand):
    
    def __init__(self, houseName: str):
        self.houseName = houseName
    
    async def execute(self, bot: Bot, cmd: Command):
        await bot.ensure_leave_from_combat()
            
        bot.is_joining_map = True
        msg = f"%xt%zm%house%1%{self.houseName}%"
        bot.write_message(msg)
        
    def to_string(self):
        return f"Goto house : {self.houseName}"