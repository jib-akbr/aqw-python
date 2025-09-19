import importlib

from colorama import Fore
from core.bot import Bot
import commands as cmd
import asyncio

username = input("Username: ")
password = input("Password: ")
server = input("Server: ")
bot_path = input(f"Bot path (e.g., {Fore.BLUE}bot.rep.yew_mountain{Fore.RESET}): ")

# Initialize bot
b = Bot(
    roomNumber=9099, 
    itemsDropWhiteList=[
        "Astral Ephemerite Essence",
        "Belrot the Fiend Essence",
        "Black Knight Essence",
        "Tiger Leech Essence",
        "Carnax Essence",
        "Chaos Vordred Essence",
        "Dai Tengu Essence",
        "Unending Avatar Essence",
        "Void Dragon Essence",
        "Creature Creation Essence",
        "Void Aura"
    ], 
    showLog=True, 
    showDebug=False,
    showChat=True,
    isScriptable=True,
    followPlayer=None,
    slavesPlayer=[],
    farmClass="Legion Revenant",
    soloClass="Void HighLord")
b.set_login_info(username, password, server)

bot_path = bot_path
try:
    bot_class = importlib.import_module(bot_path)
    print(f"starting bot: {bot_path.split('.')[-1]}")
    asyncio.run(b.start_bot(bot_class.main))
except ModuleNotFoundError as e:
    print(f"Error: {e}")
