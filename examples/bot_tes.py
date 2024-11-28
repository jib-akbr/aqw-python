from core.bot import Bot
import commands as cmd
from templates import attack
from templates.general import un_bank_items

# Initialize variables
drop_whitelist = [
        "Unidentified 19",
        "Unidentified 13",
        "Tainted Gem",
        "Dark Crystal Shard",
        "Diamond of Nulgath",
        "Voucher of Nulgath",
        "Voucher of Nulgath (non-mem)",
        "Random Weapon of Nulgath",
        "Gem of Nulgath",
        "Relic of Chaos"
    ]
    
# Initialize bot
b = Bot(
    roomNumber= 9099, 
    itemsDropWhiteList= drop_whitelist, 
    cmdDelay= 1000,
    showLog= True, 
    showDebug= False,
    showChat= True
)
b.set_login_info("u", "u", "alteon")

# Arrange commands
b.add_cmds([
        *un_bank_items(items= drop_whitelist),
        cmd.RegisterQuestCmd(2857),
        cmd.JoinMapCmd("escherion"),
        cmd.JumpCmd("Boss", "Left"),
        cmd.LabelCmd("ATK"),
        *attack.attack_monster(monster_name= "Staff of Inversion,Escherion"),
        cmd.ToLabelCmd("ATK"),
        cmd.StopBotCmd()
    ])

# Start bot
b.start_bot()