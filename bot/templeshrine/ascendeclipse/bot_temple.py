import importlib
from bot.templeshrine.ascendeclipse import config
from core.bot import Bot
import asyncio
from colorama import Fore

input_str = input("Select bot [1-4] : ")
input_int = int(input_str)

selected_slave = config.slaves[input_int - 1]

print(f"Bot selected : {Fore.YELLOW}{selected_slave.bot_path.split('.')[-1]}{Fore.RESET}")
print(f"Account config : {Fore.YELLOW}{selected_slave.username.upper()} - {selected_slave.char_class}{Fore.RESET}")

# Initialize bot
b = Bot(
    roomNumber=9099, 
    itemsDropWhiteList=[
        "Sliver of Sunlight",
        "Sliver of Moonlight",
        "Ecliptic Offering",
    ], 
    showLog=True, 
    showDebug=True,
    showChat=True,
    isScriptable=True,
    followPlayer=config.slaves[0].username.lower(),
    slavesPlayer=[slave.username for slave in config.slaves],
    farmClass=selected_slave.char_class,
)
b.set_login_info(selected_slave.username, selected_slave.password, config.server)

bot_path = selected_slave.bot_path
try:
    bot_class = importlib.import_module(bot_path)
    print(f"starting bot: {bot_path.split('.')[-1]}")
    asyncio.run(b.start_bot(bot_class.main))
except ModuleNotFoundError as e:
    print(f"Error: {e}")
