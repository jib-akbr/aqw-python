import importlib
from bot.templeshrine.solsticemoon import config
from core.bot import Bot
import asyncio

slave_index = 1

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
    followPlayer=config.main_account,
    slavesPlayer=config.slaves,
    farmClass=config.slaves[slave_index]
    )
b.set_login_info(config.slaves[slave_index], config.slaves_passwords[slave_index], config.server)

bot_path = config.slave_bot_path
try:
    bot_class = importlib.import_module(bot_path)
    print(f"starting bot: {bot_path.split('.')[-1]}")
    asyncio.run(b.start_bot(bot_class.main))
except ModuleNotFoundError as e:
    print(f"Error: {e}")
