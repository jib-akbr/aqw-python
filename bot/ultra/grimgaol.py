from core.bot import Bot
from core.command import Command
from templates.hunt import hunt_item

class Grimgaol:
    def __init__(self, cmd: Command, one_time: bool = True):
        # dont change this part
        self.cmd: Command = cmd
        self.ONE_TIME: bool = one_time
        self.VDK = "Verus DoomKnight"
        self.VHL = "Void Highlord"
        self.AM = "ArchMage"

        # fill this with the item name
        # weapons
        self.DAUNTLESS = "Malgor's ShadowFlame Blade"
        self.ELYSIUM = "Dual Exalted Apotheosis"
        self.VALIANCE = "Exalted Apotheosis"
        
        # helm
        self.ANIMA = "ArchMage's Cowl"
        self.PNEUMA = "Head of the Legion Beast"
        self.LUCK_HELM = "Awescended Omni Cowl"

        # cape
        self.VAINGLORY = "Arch DoomKnight Cape"
        self.PENITENCE = "Arch DoomKnight Cape Sword"

    async def main(self):
        while self.cmd.is_still_connected():
            await self.cmd.send_packet("%xt%zm%dungeonQueue%16424%grimgaol%")
            await self.cmd.sleep(2000)

            await self.Enter()
            await self.R2()
            await self.RVDK("r3")
            await self.RVDK("r4")
            await self.R5()
            await self.R6()
            await self.RVDK("r7")
            await self.RVDK("r8")
            await self.R9()
            await self.R10()
            await self.RVDK("r11")
            await self.RVDK("r12")

            await self.cmd.ensure_accept_quest(9467)
            await self.cmd.turn_in_quest(9467)

            if self.ONE_TIME:
                break

        self.cmd.stop_bot("FINISHED GRIMGAOL")
    
    async def Enter(self):
        print("starting Enter")
        await self.cmd.jump_cell("Enter", "Spawn")

        await self.cmd.equip_item(self.VHL)
        await self.cmd.equip_item(self.DAUNTLESS)
        await self.cmd.equip_item(self.ANIMA)
        await self.cmd.equip_item(self.VAINGLORY)

        skill_list = [1,2,4]
        skill_index = 0

        while self.cmd.is_monster_alive("Grimskull?") and self.cmd.is_still_connected():
            if self.cmd.bot.player.getLastTarget() != None:
                if self.cmd.bot.player.getLastTarget().getAura("Talon Twisting") != None:
                    # print("arua Talon Twisting detected. attack stopped")
                    await self.cmd.sleep(200)
                    continue
            await self.cmd.use_skill(0, "Grimskull?")
            await self.cmd.use_skill(skill_list[skill_index], "Grimskull?")
            skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)
        print("finished Enter")
    
    async def R2(self):
        print("starting r2")

        await self.cmd.jump_cell("r2", "Left")

        await self.cmd.equip_item(self.VHL)
        await self.cmd.equip_item(self.DAUNTLESS)
        await self.cmd.equip_item(self.ANIMA)
        await self.cmd.equip_item(self.VAINGLORY)

        skill_list = [1,2,4,2,3,2]
        skill_index = 0

        monster_name = "Grim Bomb"

        while self.cmd.is_monster_alive(monster_name) and self.cmd.is_still_connected():
            await self.cmd.use_skill(0, monster_name)
            if self.cmd.bot.player.canUseSkill(skill_list[skill_index]):
                await self.cmd.use_skill(skill_list[skill_index], monster_name)
                skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)
        print("finished r2")

    async def RVDK(self, cell: str):
        print(f"starting {cell}")

        await self.cmd.jump_cell(cell, "Left")

        await self.cmd.equip_item(self.VDK)
        await self.cmd.equip_item(self.DAUNTLESS)
        await self.cmd.equip_item(self.ANIMA)
        await self.cmd.equip_item(self.PENITENCE)

        skill_list = [1,3,4]
        skill_index = 0

        monster_name = "*"
        if cell == "r3":
            monster_name = "Empress Angler"
        elif cell == "r4" or cell == "r8":
            monster_name = "Treasure Chest"
        elif cell == "r7":
            monster_name = "Emperor Angler"
        elif cell == "r11":
            monster_name = "Mechabinky & Raxborg"
        elif cell == "r12":
            monster_name = "Grimskull"

        while self.cmd.is_monster_alive(monster_name) and self.cmd.is_still_connected():
            mons_hp = self.cmd.get_monster_hp(monster_name)
            if mons_hp and mons_hp > -1:
                print(f"{monster_name}: {mons_hp} : {self.cmd.get_monster_hp_percentage(monster_name)}%")
            print(f"{self.cmd.bot.player.CURRENT_HP} / {self.cmd.bot.player.MAX_HP}")
            if self.cmd.hp_below_percentage(90):
                await self.cmd.use_skill(2, monster_name)
            await self.cmd.use_skill(0, monster_name)
            await self.cmd.use_skill(skill_list[skill_index], monster_name)
            skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)

        print(f"finished {cell}")

    async def R5(self):
        print(f"starting r5")

        await self.cmd.jump_cell("r5", "Left")
        await self.cmd.bank_to_inv(self.AM)
        await self.cmd.equip_item(self.AM)
        await self.cmd.equip_item(self.ELYSIUM)
        await self.cmd.equip_item(self.PNEUMA)
        await self.cmd.equip_item(self.PENITENCE)

        skill_list = [2,3,1]
        skill_index = 0
        monster_name = "Reinforced Shelleton"

        while self.cmd.is_monster_alive(monster_name) and self.cmd.is_still_connected():
            # Arcane Flux -> Corporeal Ascension
            has_corp = self.cmd.bot.player.hasAura("Corporeal Ascension")
            if not has_corp:
                await self.cmd.wait_use_skill(1)
                await self.cmd.wait_use_skill(4)
            # print(f"{self.cmd.bot.player.CURRENT_HP} / {self.cmd.bot.player.MAX_HP}")
            await self.cmd.use_skill(0, monster_name)
            if self.cmd.bot.player.canUseSkill(skill_list[skill_index]):
                await self.cmd.use_skill(skill_list[skill_index], monster_name)
                skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)

        print(f"finished r5")

    async def R6(self):
        print(f"starting r6")

        await self.cmd.jump_cell("r6", "Left")
        await self.cmd.equip_item(self.VHL)
        await self.cmd.equip_item(self.VALIANCE)
        await self.cmd.equip_item(self.LUCK_HELM)
        await self.cmd.equip_item(self.VAINGLORY)

        skill_list = [1,2,3,4]
        skill_index = 0
        
        monster_id = ["id.10", "id.11", "id.12"]
        monster_index = 0
        monster_to_attack = monster_id[monster_index]
        while self.cmd.is_monster_alive("*") and self.cmd.is_still_connected():
            last_target = self.cmd.bot.player.getLastTarget()
            if last_target:
                print(f"{last_target.mon_name} ({last_target.mon_map_id}): {last_target.current_hp} / {last_target.max_hp} : {self.cmd.get_monster_hp_percentage(f'id.{last_target.mon_map_id}')}%")
                if last_target.hasAura("Crit Damage Amplified"):
                    found = False
                    for mon in self.cmd.bot.monsters:
                        if f"id.{mon.mon_map_id}" in monster_id and not mon.hasAura("Crit Damage Amplified"):
                            monster_to_attack = f"id.{mon.mon_map_id}"
                            found = True
                            break
                    if not found:
                        await self.cmd.sleep(200)
                        continue
            await self.cmd.use_skill(0, monster_to_attack)
            if self.cmd.bot.player.CURRENT_HP > 2500 and (skill_list[skill_index] == 1 or skill_list[skill_index] == 3):
                await self.cmd.use_skill(skill_list[skill_index], monster_to_attack)
            else:
                await self.cmd.use_skill(skill_list[skill_index], monster_to_attack)
            skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)

        print("finished r6")

    async def R9(self):
        print(f"starting r9")

        await self.cmd.jump_cell("r9", "Left")
        await self.cmd.equip_item(self.VHL)
        await self.cmd.equip_item(self.DAUNTLESS)
        await self.cmd.equip_item(self.ANIMA)
        await self.cmd.equip_item(self.VAINGLORY)

        skill_list = [1,2,3,4]
        skill_index = 0

        monster_name = "Rick, Grim Soldier"

        while self.cmd.is_monster_alive("*") and self.cmd.is_still_connected():
            await self.cmd.use_skill(0, monster_name)
            if self.cmd.bot.player.CURRENT_HP > 2500 and (skill_list[skill_index] == 1 or skill_list[skill_index] == 3):
                await self.cmd.use_skill(skill_list[skill_index], monster_name)
            else:
                await self.cmd.use_skill(skill_list[skill_index])
            skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)

        print("finished r9")

    async def R10(self):
        print(f"starting r10")

        await self.cmd.jump_cell("r10", "Left")
        await self.cmd.bank_to_inv(self.AM)
        await self.cmd.equip_item(self.AM)
        await self.cmd.equip_item(self.ELYSIUM)
        await self.cmd.equip_item(self.PNEUMA)
        await self.cmd.equip_item(self.PENITENCE)

        skill_list = [2,3,1]
        skill_index = 0
        monster_name = "Mechro Lich,Rampaging Cyborg"

        while self.cmd.is_monster_alive("*") and self.cmd.is_still_connected():
            # Arcane Flux -> Corporeal Ascension
            has_corp = self.cmd.bot.player.hasAura("Corporeal Ascension")
            if not has_corp:
                await self.cmd.wait_use_skill(1)
                await self.cmd.wait_use_skill(4)
            print(f"{self.cmd.bot.player.CURRENT_HP} / {self.cmd.bot.player.MAX_HP}")
            await self.cmd.use_skill(0, monster_name)
            if self.cmd.bot.player.canUseSkill(skill_list[skill_index]):
                await self.cmd.use_skill(skill_list[skill_index], monster_name)
                skill_index = (skill_index + 1) % len(skill_list)
            await self.cmd.sleep(200)

        print(f"finished r10")


# MAIN
async def main(cmd: Command):
    cmdBot: Grimgaol = Grimgaol(cmd)
    await cmdBot.main()
