from core.bot import Bot
from templates import afk, attack
import commands as cmd

# Initialize bot
b = Bot(
    roomNumber="9099", 
    itemsDropWhiteList=["Undead Energy", "Undead Essence", "Bone Dust"], 
    cmdDelay=500,
    showLog=True, 
    showDebug=False,
    showChat=True)
b.set_login_info("username", "password", "twilly")

# Initialize variables
atk = attack.generalAttack
itemName = "Undead Essence"
itemQty = 45

# Arrange commands
b.add_cmds([
        cmd.IsInBankCmd(itemName),
        cmd.BankToInvCmd(itemName),
        cmd.IsInInvCmd(itemName, itemQty, operator=">="),
        cmd.StopBotCmd(),
        cmd.JoinMapCmd("battleunderb"),
        cmd.JumpCmd("Enter", "Spawn"),
    ] + atk + [
        cmd.IsInInvCmd(itemName, itemQty, operator="<="),
        cmd.UpIndexCmd(len(atk)+1),
        cmd.InvToBankCmd(itemName),
        cmd.StopBotCmd()
    ])

# Start bot
b.start_bot()