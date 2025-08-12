import importlib
from core.bot import Bot
import asyncio
from bot.templeshrine.midnightsun import config

# Initialize bot
b = Bot(
    roomNumber=9099, 
    itemsDropWhiteList=[
        "Sliver of Sunlight",
        "Sliver of Moonlight",
        "Ecliptic Offering",
    ], 
    showLog=True, 
    showDebug=False,
    showChat=True,
    isScriptable=True,
    slavesPlayer=config.slaves,
    farmClass=config.main_class
    )
b.set_login_info(config.main_account, config.main_password, config.server)

bot_path = config.main_bot_path
try:
    bot_class = importlib.import_module(bot_path)
    print(f"starting bot: {bot_path.split('.')[-1]}")
    asyncio.run(b.start_bot(bot_class.main))
except ModuleNotFoundError as e:
    print(f"Error: {e}")
