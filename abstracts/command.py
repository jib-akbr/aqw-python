from abc import ABC, abstractmethod
from core.bot import Bot

class Command(ABC):
    
    skip_delay = False
    
    @abstractmethod
    async def execute(self, bot: Bot):
        pass
        
    @abstractmethod
    def to_string(self):
        return "Command"