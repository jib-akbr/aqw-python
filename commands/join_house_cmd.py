from core.bot import Bot
from abstracts.command import Command

class JoinHouseCmd(Command):
    
    def __init__(self, houseName: str):
        self.houseName = houseName
    
    def execute(self, bot: Bot):
        bot.is_joining_map = True
        msg = f"%xt%zm%house%1%{self.houseName}%"
        bot.write_message(msg)
        bot.doSleep(500)
        
    def to_string(self):
        return f"Goto house : {self.houseName}"