from core.bot import Bot
from abstracts.command import Command
from colorama import Fore

class StopBotCmd(Command):
    
    def __init__(self, msg: str = ""):
        self.msg = msg
    
    async def execute(self, bot: Bot):
        print(Fore.RED + self.msg + Fore.RESET)
        bot.stop_bot()
        
    def to_string(self):
        return "Stop bot"