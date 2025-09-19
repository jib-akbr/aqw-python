import asyncio
import json

from colorama import Fore

from core.commands.base import _CommandBase, check_alive

class UtilityCommands(_CommandBase):
    """General-purpose helpers shared across categories."""

    def stopBot(self, msg: str = ""):
        print(Fore.RED + msg + Fore.RESET)
        print(Fore.RED + "stop bot: " + self.bot.player.USER + Fore.RESET)
        self.bot.stop_bot()

    async def send_chat(self, message: str):
        await self.send_packet(f"%xt%zm%message%{self.bot.areaId}%{message}%zone%")

    async def rest(self):
        await self.send_packet(f"%xt%zm%restRequest%1%%")

    @check_alive
    async def sleep(self,  milliseconds: int) -> None:
        await asyncio.sleep(milliseconds/1000)

    async def send_packet(self, packet: str):
        if not self.is_still_connected():
            return
        self.bot.write_message(packet)
        await asyncio.sleep(0.5)

    def is_valid_json(self, s):
        try:
            json.loads(s)
            return True
        except json.JSONDecodeError:
            return False
