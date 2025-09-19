import asyncio
import json

from colorama import Fore

from core.commands.base import _CommandBase, check_alive

class UtilityCommands(_CommandBase):
    """General-purpose helpers shared across categories."""

    def stopBot(self, msg: str = "") -> None:
        """Print a stop message and terminate the bot session."""
        print(Fore.RED + msg + Fore.RESET)
        print(Fore.RED + "stop bot: " + self.bot.player.USER + Fore.RESET)
        self.bot.stop_bot()

    async def send_chat(self, message: str) -> None:
        """Send a zone chat message through the server packet API."""
        await self.send_packet(f"%xt%zm%message%{self.bot.areaId}%{message}%zone%")

    async def rest(self) -> None:
        """Request the rest action from the server."""
        await self.send_packet(f"%xt%zm%restRequest%1%%")

    @check_alive
    async def sleep(self,  milliseconds: int) -> None:
        """Asynchronously sleep for the requested number of milliseconds."""
        await asyncio.sleep(milliseconds/1000)

    async def send_packet(self, packet: str) -> None:
        """Send a raw packet to the server after validating connectivity."""
        if not self.is_still_connected():
            return
        self.bot.write_message(packet)
        await asyncio.sleep(0.5)

    def is_valid_json(self, s: str) -> bool:
        """Return True when the provided string parses as JSON."""
        try:
            json.loads(s)
            return True
        except json.JSONDecodeError:
            return False
