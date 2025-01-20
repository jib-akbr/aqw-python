from core.bot import Bot
from core.commands import Command
from core.commands import Command
from abstracts.base_command import BaseCommand

class JoinMapCmd(BaseCommand):
    
    def __init__(self, mapName: str, roomNumber: int = None, safeLeave: bool = True):
        self.mapName = mapName
        self.roomNumber = roomNumber
        self.safeLeave = safeLeave
    
    async def execute(self, bot: Bot, cmd: Command):
        cmd.join_map(self.mapName, self.roomNumber, self.safeLeave)
        
    def to_string(self):
        if self.roomNumber != None:
            return f"Join : {self.mapName}-{self.roomNumber}"
        else:
            return f"Join : {self.mapName}"