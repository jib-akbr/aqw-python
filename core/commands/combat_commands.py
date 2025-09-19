import asyncio
from datetime import datetime
from core.commands.base import _CommandBase, check_alive
from model.inventory import ItemType
from model.monster import Monster
from typing import Optional
    
class CombatCommands(_CommandBase):
    """Combat utilities such as skills and aggro management."""
    skill_reload_time: int = 0

    @check_alive
    async def leave_combat(self, safeLeave: bool = True) -> None:
        """Leave combat and optionally jump back to spawn.

        Args:
            safeLeave (bool): Jump to the Enter/Spawn cell after leaving combat when True.

        Returns:
            None: Always returns None; the bot actions run asynchronously.
        """
        await self.bot.ensure_leave_from_combat(always=True)
        if safeLeave:
            await self.jump_cell("Enter", "Spawn")

    @check_alive
    async def jump_to_monster(self, monsterName: str, byMostMonster: bool = True, byAliveMonster: bool = False) -> None:
        """Jump to the cell that currently hosts the requested monster.

        Args:
            monsterName (str): Display name or ``id.X`` identifier for the monster.
            byMostMonster (bool): Prefer the cell with the highest monster population when True.
            byAliveMonster (bool): Prefer a cell that still has the monster alive when True.

        Returns:
            None: The coroutine adjusts player position and exits.
        """
        if monsterName.startswith('id.'):
            monsterName = monsterName.split('.')[1]
        for monster in self.bot.monsters:
            if (monster.mon_name.lower() == monsterName.lower() or monster.mon_map_id == monsterName )\
                    and monster.is_alive \
                    and self.bot.player.CELL == monster.frame:
                return

        # Hunt monster in other cell
        if byMostMonster or byAliveMonster:
            cell = self.bot.find_best_cell(monsterName, byMostMonster, byAliveMonster)
            if cell:
                if cell == self.bot.player.CELL:
                    return
                self.bot.jump_cell(cell, "Left")
                await asyncio.sleep(1)
                return
        for monster in self.bot.monsters:
            if (monster.mon_name.lower() == monsterName.lower() or monster.mon_map_id == monsterName )\
                    and monster.is_alive \
                    and self.bot.player.CELL != monster.frame:
                # TODO need to handle the rigth pad
                self.bot.jump_cell(monster.frame, "Left")
                await asyncio.sleep(1)
                return

    @check_alive
    async def wait_use_skill(self, index: int, target_monsters: str = "*") -> None:
        """Wait until a skill is ready before casting it.

        Args:
            index (int): Skill slot to trigger.
            target_monsters (str): Comma-separated monster names or ``id.X`` identifiers to focus.

        Returns:
            None: The coroutine finishes once the skill has been used.
        """
        while not self.bot.player.canUseSkill(int(index)):
            await self.sleep(100)
        await self.use_skill(index, target_monsters)
        
    def check_is_skill_safe(self, skill: int) -> bool:
        """Return whether a skill is safe to use at the current HP threshold.

        Args:
            skill (int): Skill slot that is about to be executed.

        Returns:
            bool: True when the skill can be used safely for the equipped class.
        """
        conditions = {
            "void highlord": {
                "hp_threshold": 50, # in percentage of current hp from max hp
                "skills_to_check": [1, 3],
                "condition": lambda hp, threshold: hp < threshold
            },
            "scarlet sorceress": {
                "hp_threshold": 50,
                "skills_to_check": [1, 4],
                "condition": lambda hp, threshold: hp < threshold
            },
            "dragon of time": {
                "hp_threshold": 40,
                "skills_to_check": [1, 3],
                "condition": lambda hp, threshold: hp < threshold
            },
            # "archpaladin": {
            #     "hp_threshold": 70,
            #     "skills_to_check": [2],
            #     "condition": lambda hp, threshold: hp > threshold
            # },
        }
        # Get the class and its conditions
        equipped_class = self.bot.player.get_equipped_item(ItemType.CLASS)
        if equipped_class:
            if equipped_class.item_name in conditions:
                condition = conditions[equipped_class.item_name]
                current_hp = self.bot.player.CURRENT_HP
                max_hp = self.bot.player.MAX_HP
                # Check if the current conditions match
                if skill in condition["skills_to_check"] and condition["condition"]((current_hp / max_hp) * 100, condition["hp_threshold"]):
                    return False
        return True

    @check_alive
    async def use_skill(self,  
                        index: int = 0, 
                        target_monsters: str = "*", 
                        hunt: bool = False, 
                        buff_only: bool = False,
                        reload_delay: int = 500
        ) -> None:
        """Execute a skill with optional hunting, targeting, and cooldown handling.

        Args:
            index (int): Skill slot that should be triggered.
            target_monsters (str): Target filter, ``*`` for any or comma-separated list.
            hunt (bool): When True, jump to the monster before casting.
            buff_only (bool): Prevent damaging skills from firing when True.
            reload_delay (int): Cooldown buffer in milliseconds after casting.

        Returns:
            None: The coroutine schedules the skill usage and exits.
        """
        if not self.bot.player.canUseSkill(int(index)) or not self.check_is_skill_safe(int(index)):
            return

        skill = self.bot.player.SKILLS[int(index)]
        self.bot.skillAnim = skill.get("anim", None)
        max_target = int(skill.get("tgtMax", 1))
        
        wait_reload_s = (self.skill_reload_time - int(round(datetime.now().timestamp() * 1000))) / 1000
        if wait_reload_s > 0 and index != 0:
            # print(Fore.BLUE + f"[{datetime.now().strftime('%H:%M:%S')}] wait reload skill:{index} cd:{wait_reload_s:.2f} s" + Fore.RESET)
            await self.sleep(wait_reload_s*1000)

        if skill["tgt"] == "h": 
            priority_monsters_id = []
            if hunt and len(target_monsters.split(",")) == 1 and target_monsters != "*":
                await self.jump_to_monster(target_monsters, byAliveMonster=True)
            cell_monsters_id = [mon.mon_map_id for mon in self.bot.monsters if mon.frame == self.bot.player.CELL and mon.is_alive]
            cell_monsters = [mon for mon in self.bot.monsters if mon.frame == self.bot.player.CELL and mon.is_alive]
            final_ids = []
            if target_monsters != "*":
                # Mapping priority_monsters_id
                target_ids = []
                target_names = []
                for target_monster in target_monsters.split(','):
                    if target_monster.startswith('id.'):
                        target_ids.append(target_monster.split('.')[1])
                    else:
                        target_names.append(target_monster.lower())

                # Step 1: build a map of alive monsters in current cell
                alive_monsters = {mon.mon_map_id: mon for mon in self.bot.monsters if mon.frame == self.bot.player.CELL and mon.is_alive}

                priority_monsters_id = []

                # Step 2: follow *input* order strictly
                for target in target_monsters.split(','):
                    if target.startswith("id."):
                        mon_id = target.split(".")[1]
                        if mon_id in alive_monsters:
                            priority_monsters_id.append(mon_id)
                    else:
                        name = target.lower()
                        for mon in self.bot.monsters:
                            if mon.frame == self.bot.player.CELL and mon.is_alive and mon.mon_name.lower() == name:
                                priority_monsters_id.append(mon.mon_map_id)

                # Step 3: merge into cell_monsters_id (dedup, keep priority first)
                final_ids = []
                seen = set()

                # First: priority in order
                for mon_id in priority_monsters_id:
                    if mon_id not in seen:
                        final_ids.append(mon_id)
                        seen.add(mon_id)

                # Then: the rest
                for mon_id in cell_monsters_id:
                    if mon_id not in seen:
                        final_ids.append(mon_id)
                        seen.add(mon_id)

            else:
                cell_monsters.sort(key=lambda m: m.current_hp)
                final_ids = [mon.mon_map_id for mon in cell_monsters]
            if index == 5:
                self.bot.use_scroll(final_ids, max_target)
            if index < 5 and len(final_ids) > 0 and not buff_only:
                self.bot.use_skill_to_monster("a" if index == 0 else index, final_ids, max_target)
        elif skill["tgt"] == "f":
            self.bot.use_skill_to_player(index, max_target)
        elif skill["tgt"] == "s":
            self.bot.use_skill_to_myself(index)
        
        await self.sleep(200)
        self.bot.player.updateNextUse(index) # do this if skills is REALLY exetuced
    
        self.skill_reload_time = int(round(datetime.now().timestamp() * 1000)) + reload_delay

    @check_alive
    def do_pwd(self, monster_id: str) -> None:
        """Send a raw PWD packet to the server for a specific monster.

        Args:
            monster_id (str): Monster identifier to include in the packet payload.

        Returns:
            None: The message is sent and no value is returned.
        """
        # %xt%zm%gar%1%3%p6>m:1%wvz%
        self.bot.write_message(f"%xt%zm%gar%1%3%p6>m:{monster_id}%wvz%")

    def start_aggro_by_cell(self, cells: list[str], delay_ms : int = 500) -> None:
        """Start aggroing every monster found in the provided cells.

        Args:
            cells (list[str]): Cell names to scan for monsters.
            delay_ms (int): Delay between aggro commands in milliseconds.

        Returns:
            None: Delegates to start_aggro when monsters are present.
        """
        mons_id: list[str] = []
        for monster in self.bot.monsters:
            if monster.frame in cells:
                mons_id.append(str(monster.mon_map_id))

        if len(mons_id) == 0:
            return
        
        self.start_aggro(mons_id, delay_ms)

    def start_aggro(self, mons_id: list[str], delay_ms: int = 500) -> None:
        """Enable the aggro handler for the supplied monster identifiers.

        Args:
            mons_id (list[str]): Monster identifiers to keep aggroed.
            delay_ms (int): Delay between aggro ticks in milliseconds.

        Returns:
            None: Updates the bot state and starts the aggro task.
        """
        self.stop_aggro()
        self.bot.is_aggro_handler_task_running = True
        self.bot.aggro_mons_id = mons_id
        self.bot.aggro_delay_ms = delay_ms
        self.bot.run_aggro_hadler_task()

    def stop_aggro(self) -> None:
        """Stop the aggro handler and clear tracked monsters.

        Returns:
            None: Clears aggro state without returning a value.
        """
        self.bot.is_aggro_handler_task_running = False
        self.bot.aggro_mons_id = []

    def is_monster_alive(self, monster: str = "*") -> bool:
        """Check whether a monster is alive in the player's current cell.

        Args:
            monster (str): Name or ``id.X`` identifier of the monster, ``*`` for any.

        Returns:
            bool: True when a matching live monster is found in the cell.
        """
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.is_alive and mon.frame == self.bot.player.CELL:
                if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                    return True
                elif monster == "*":
                    return True
        return False

    @check_alive
    def get_monster_hp(self, monster: str) -> int:
        """Get the current HP of the requested monster.

        Args:
            monster (str): Name or ``id.X`` identifier of the monster, ``*`` for any.

        Returns:
            int: Current HP, or -1 when the monster is not found.
        """
        if monster == None:
            return -1
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster and mon.is_alive:
                return mon.current_hp
            elif monster == "*":
                return mon.current_hp
        # this mean not get the desired monster
        return -1

    def get_monster_hp_percentage(self, monster: str) -> int:
        """Get the remaining HP of a monster as a percentage.

        Args:
            monster (str): Name or ``id.X`` identifier of the monster, ``*`` for any.

        Returns:
            int: Rounded HP percentage, or -1 when the monster is missing.
        """
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                return round(((mon.current_hp/mon.max_hp)*100), 2)
            elif monster == "*":
                return round(((mon.current_hp/mon.max_hp)*100), 2)
        # this mean not get the desired monster
        return -1

    def get_monster(self, monster: str) -> Optional[Monster]:
        """Return the monster object that matches the provided identifier.

        Args:
            monster (str): Name or ``id.X`` identifier of the monster.

        Returns:
            Monster or None: Monster instance when found, otherwise None.
        """
        if monster.startswith('id.'):
            monster = monster.split('.')[1]
        for mon in self.bot.monsters:
            if mon.mon_name.lower() == monster.lower() or mon.mon_map_id == monster:
                return mon
        return None

    @check_alive
    def hp_below_percentage(self, percent: int) -> bool:
        """Check if the player HP is below the requested percentage.

        Args:
            percent (int): HP threshold to compare against.

        Returns:
            bool: True when the player HP percentage is lower than the threshold.
        """
        return ((self.bot.player.CURRENT_HP / self.bot.player.MAX_HP) * 100) < percent
