from core.bot import Bot
from core.commands import Command
from core.commands import Command
from abstracts.base_command import BaseCommand

class JoinMapCmd(BaseCommand):
    
    def __init__(self, mapName: str, roomNumber: int = None):
        self.mapName = mapName
        self.roomNumber = roomNumber
    
    async def execute(self, bot: Bot, cmd: Command):
        if bot.strMapName.lower() == self.mapName.lower():
            return
        bot.is_joining_map = True
        await bot.ensure_leave_from_combat(always=True)
        
        if self.roomNumber != None:
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}-{self.roomNumber}%"
        elif bot.roomNumber != None:
            self.roomNumber = bot.roomNumber
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}-{bot.roomNumber}%"
        else:
            msg = f"%xt%zm%cmd%1%tfer%{bot.player.USER}%{self.mapName}%"
        bot.write_message(msg)
        
    def to_string(self):
        if self.roomNumber != None:
            return f"Join : {self.mapName}-{self.roomNumber}"
        else:
            return f"Join : {self.mapName}"