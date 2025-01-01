import os
from dotenv import load_dotenv
import importlib
from core.bot import Bot
from templates.attack import generalAttack
import commands as cmd
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
# Or you can just directly write the creds
username = os.getenv("USERNAME_AQW")
password = os.getenv("PASSWORD_AQW")
server = os.getenv("SERVER")

# directly
# username = "username"
# password = "password"
# server = "alteon"

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
    farmClass="Legion Revenant")
b.set_login_info(username, password, server)

bot_path = "bot.void_aura"
try:
    bot_class = importlib.import_module(bot_path)
    print(f"starting bot: {bot_path.split('.')[-1]}")
    asyncio.run(b.start_bot(bot_class.main))
except ModuleNotFoundError as e:
    print(f"Error: {e}")
