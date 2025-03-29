from core.bot import Bot
import commands as cmd
from templates import attack

b = Bot(
    roomNumber=9909,
    itemsDropWhiteList=["Stars Destroyed"],
    cmdDelay=500,
    showLog=True,
    showDebug=False,
    showChat=True
)

b.set_login_info("u", "p", "twilly")

atk = attack.generalAttack
itemName = "Stars Destroyed"
itemQty = 1000000

b.add_cmds([
    cmd.EquipItemCmd("Legion Revenant"),
    cmd.IsInBankCmd(itemName),
    cmd.BankToInvCmd(itemName),
    cmd.JoinMapCmd("starfield",999999),
    cmd.AcceptQuestCmd(9818),
    cmd.SleepCmd(1000),
    cmd.JumpCmd("r3", "Spawn"),
    cmd.LabelCmd("ATK")
] + atk + [
    cmd.IsInInvCmd(itemName, itemQty),
    cmd.StopBotCmd(),
    cmd.ToLabelCmd("ATK")
])

b.start_bot()