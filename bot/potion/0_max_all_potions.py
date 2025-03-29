from core.bot import Bot
from core.commands import Command
from bot.potion.core_potion import PotentDestructionElixir, PotentHonorMalice, PotentMalevolence, PotentRevitalizeElixir, PotentBattleElixir, SageTonic, FateTonic, BodyTonic, MightTonic

# get the maxiumum quant of potions
async def main(cmd: Command):

    await PotentHonorMalice(cmd.bot, cmd)
    await PotentMalevolence(cmd.bot, cmd)
    await SageTonic(cmd.bot, cmd)
    await PotentDestructionElixir(cmd.bot, cmd)
    await PotentRevitalizeElixir(cmd.bot, cmd)
    await PotentBattleElixir(cmd.bot, cmd)
    await FateTonic(cmd.bot, cmd)
    await BodyTonic(cmd.bot, cmd)
    await MightTonic(cmd.bot, cmd)

    cmd.stopBot("MAX ALL POTIONS DONE")