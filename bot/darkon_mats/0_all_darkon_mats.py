from bot.darkon_mats.core_darkon_mats import a_melody, ancient_remnant, astravian_medal, bandits_correspondence, bounty_hunter_dubloon, darkons_receipts_binky, darkons_receipts_tower_of_doom, las_gratitude, mourning_flower, sukis_prestige, unfinished_musical_score
from core.bot import Bot
from core.commands import Command

# get the maxiumum quant of darkon mats
async def main(bot: Bot):
    cmd = Command(bot)

    await a_melody(cmd)
    await ancient_remnant(cmd)
    await astravian_medal(cmd)
    await bandits_correspondence(cmd)
    await bounty_hunter_dubloon(cmd)
    # await darkons_receipts_binky(cmd)
    # await darkons_receipts_tower_of_doom(cmd)
    await las_gratitude(cmd)
    await mourning_flower(cmd)
    await sukis_prestige(cmd)
    await unfinished_musical_score(cmd)