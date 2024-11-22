from core.bot import Bot
from abstracts.command import Command

class JoinMapCmd(Command):
    
    def __init__(self, mapName: str, roomNumber: int = None):
        self.mapName = mapName
        self.roomNumber = roomNumber
    
    def execute(self, bot: Bot):
        bot.is_joining_map = True
        if self.roomNumber != None:
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}-{self.roomNumber}%"
        elif bot.roomNumber != None:
            self.roomNumber = bot.roomNumber
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}-{bot.roomNumber}%"
        else:
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}%"
        bot.write_message(msg)
        bot.doSleep(500)
        
    def to_string(self):
        if self.roomNumber != None:
            return f"Join : {self.mapName}-{self.roomNumber}"
        else:
            return f"Join : {self.mapName}"