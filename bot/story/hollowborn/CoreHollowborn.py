from core.bot import Bot
from core.commands import Command
from templates.hunt import kill_quest, quest_item_req, hunt_item

async def Trygve(cmd: Command):

    while cmd.is_not_in_map("trygve"):
        await cmd.join_map("trygve")

    if cmd.bot.farmClass:
        await cmd.equip_item(cmd.bot.farmClass)

    # preload quest for faster story
    quest = 8289
    await cmd.accept_quest_bulk(quest, 10)

    # Wunjo, Reversed (8289)
    if await cmd.is_green_quest(8289):
        await kill_quest(cmd, 8289, "trygve", "Vindicator Recruit")

    # Berkana (8290)
    if await cmd.is_green_quest(8290):
        await cmd.ensure_accept_quest(8290)
        await hunt_item(cmd, map_name="trygve", item_name="Blood Eagle Feather", item_qty=9, monster_name="Blood Eagle")
        await cmd.get_map_item(9036)
        await cmd.ensure_turn_in_quest(8290)

    # Algiz, Reversed (8291)
    if await cmd.is_green_quest(8291):
        await cmd.ensure_accept_quest(8291)
        await hunt_item(cmd, map_name="trygve", item_name="Armor Chunk", item_qty=9, monster_name="Vindicator Recruit")
        await cmd.get_map_item(9037)
        await cmd.ensure_turn_in_quest(8291)

    # Gebo (8292)
    if await cmd.is_green_quest(8292):
        await cmd.ensure_accept_quest(8292)
        await hunt_item(cmd, map_name="trygve", item_name="Patch of Boar Hide", item_qty=8, monster_name="Rune Boar")
        await cmd.get_map_item(9038)
        await cmd.ensure_turn_in_quest(8292)

    # Eihwaz (8293)
    if await cmd.is_green_quest(8293):
        await cmd.ensure_accept_quest(8293)
        await cmd.get_map_item(9039, 3)
        await hunt_item(cmd, map_name="trygve", item_name="Soldiers Pacified", item_qty=9, monster_name="Vindicator Recruit")
        await cmd.ensure_turn_in_quest(8293)

    # Hagalaz (8294)
    if await cmd.is_green_quest(8294):
        await cmd.ensure_accept_quest(8294)
        await cmd.get_map_item(9040, 8)
        await cmd.ensure_turn_in_quest(8294)

    # Mannaz (8295)
    if await cmd.is_green_quest(8295):
        await cmd.ensure_accept_quest(8295)
        await hunt_item(cmd, map_name="trygve", item_name="Boar Bone", item_qty=9, monster_name="Rune Boar")
        await hunt_item(cmd, map_name="trygve", item_name="Eagle Talon", item_qty=9, monster_name="Blood Eagle")
        await cmd.ensure_turn_in_quest(8295)

    # Thurisaz (8296)
    if await cmd.is_green_quest(8296):
        await kill_quest(cmd, 8296, map_name="trygve", item_name="Vindicator Recruit")

    # Othala (8297)
    if await cmd.is_green_quest(8297):
        await cmd.ensure_accept_quest(8297)
        await hunt_item(cmd, map_name="trygve", item_name="Creature Bones", item_qty=7, monster_name="Blood Eagle")
        await hunt_item(cmd, map_name="trygve", item_name="Vindicator Defeated", item_qty=7, monster_name="Vindicator Recruit")
        await cmd.ensure_turn_in_quest(8297)

    # Isa, Reversed (8298)
    if await cmd.is_green_quest(8298):
        await kill_quest(cmd, 8298, map_name="trygve", monster_name="Gramiel")

async def NeoFortress(cmd: Command):

    while cmd.is_not_in_map("neofortress"):
        await cmd.join_map("neofortress")

    if cmd.bot.farmClass:
        await cmd.equip_item(cmd.bot.farmClass)

    # preload quest for faster story
    quest = 9281
    await cmd.accept_quest_bulk(quest, 10)

    # Watch the Light (9281)
    if await cmd.is_green_quest(9281):
        await cmd.get_map_item(11806, 9)

    # Uprootment Recruitment (9282)
    if await cmd.is_green_quest(9282):
        await kill_quest(cmd, 9282, "neofortress", "Vindicator Recruit")

    # Endless Hounding (9283)
    if await cmd.is_green_quest(9283):
        await kill_quest(cmd, 9283, "neofortress", "Vindicator Hound")

    # Mystery Creature (9284)
    if await cmd.is_green_quest(9284):
        await kill_quest(cmd, 9284, "neofortress", "Vindicator Beast")

    # Retrieve the Keys (9285)
    if await cmd.is_green_quest(9285):
        await kill_quest(cmd, 9285, "neofortress", "Vindicator Soldier")

    # Free the Prisoners (9286)
    if await cmd.is_green_quest(9286):
        await cmd.accept_quest(9286)
        await cmd.get_map_item(11807, 5)
        await cmd.turn_in_quest(9286)

    # Vindicator General (9287)
    if await cmd.is_green_quest(9287):
        await kill_quest(cmd, 9287, "neofortress", "Vindicator General")

    # De-dicated (9288)
    if await cmd.is_green_quest(9288):
        await kill_quest(cmd, 9288, "neofortress", "Vindicator Recruit")

    # Get into the Chambers (9289)
    if await cmd.is_green_quest(9289):
        await kill_quest(cmd, 9289, "neofortress", "Vindicator General")

    # Tales from the Past (9290)
    if await cmd.is_green_quest(9290):
        await cmd.accept_quest(9290)
        await cmd.get_map_item(11808)
        await cmd.turn_in_quest(9290)

async def ShadowslayerD(cmd: Command):
    while cmd.is_not_in_map("hbchallenge"):
        await cmd.join_map("hbchallenge")

async def Shadowrealm(cmd: Command):

    while cmd.is_not_in_map("shadowrealm"):
        await cmd.join_map("shadowrealm")

    quest = 9783
    await cmd.accept_quest_bulk(quest, 10)

    # The First Crumb (9783)
    if await cmd.is_green_quest(9783):
        await kill_quest(9783, "bonecastle", "Undead Guard")

    # Return to Lifeblood (9784)
    if await cmd.is_green_quest(9784):
        await kill_quest(9784, "lycan", "Sanguine")

    # Nohairatu (9785)
    if await cmd.is_green_quest(9785):
        await kill_quest(9785, "umbral", "Rapaxi")

    # Bony Hodgepodge (9786)
    if await cmd.is_green_quest(9786):
        await kill_quest(9786, "battleundera", "Bone Terror")
