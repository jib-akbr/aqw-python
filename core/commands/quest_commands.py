import asyncio
from typing import Optional

from core.commands.base import _CommandBase, check_alive

class QuestCommands(_CommandBase):
    """Quest-related automation helpers."""
    quest_to_check: Optional[int] = None
    is_green_quest_var: Optional[bool] = None
    is_completed_before_var: Optional[bool] = None

    @check_alive
    async def ensure_accept_quest(self, quest_id: int) -> None:
        while self.quest_not_in_progress(quest_id) and self.is_still_connected():
            await self.accept_quest(quest_id)
            await self.sleep(1000)
            if quest_id in self.bot.failed_get_quest_datas:
                return

    @check_alive
    async def ensure_turn_in_quest(self, quest_id: int, item_id = -1, amount = 1) -> None:
        while self.quest_in_progress(quest_id) and self.is_still_connected():
            await self.turn_in_quest(quest_id, item_id,amount)
            await self.sleep(1000)
            if quest_id in self.bot.failed_get_quest_datas:
                return
        print("quest turned in:", quest_id, item_id)

    @check_alive
    async def accept_quest(self, quest_id: int) -> None:
        self.bot.accept_quest(quest_id)
        print("trying accept quest:", quest_id)
        await asyncio.sleep(1)

    @check_alive
    async def turn_in_quest(self, quest_id: int, item_id: int = -1, qty: int = 1) -> None:
        self.quest_to_check = quest_id
        await self.bot.ensure_leave_from_combat()
        self.bot.turn_in_quest(quest_id, item_id, qty)
        await asyncio.sleep(1)

    def quest_not_in_progress(self, quest_id: int) -> bool:
        loaded_quest_ids = [loaded_quest["QuestID"] for loaded_quest in self.bot.loaded_quest_datas]
        return str(quest_id) not in str(loaded_quest_ids)

    def quest_in_progress(self, quest_id: int) -> bool:
        loaded_quest_ids = [loaded_quest["QuestID"] for loaded_quest in self.bot.loaded_quest_datas]
        return str(quest_id) in str(loaded_quest_ids)

    def can_turnin_quest(self, questId: int) -> bool:
        return self.bot.can_turn_in_quest(questId)

    @check_alive
    async def is_green_quest(self, quest_id: int) -> bool:
        await self.turn_in_quest(quest_id)
        while(self.is_still_connected()):
            if self.is_green_quest_var is not None:
                output = self.is_green_quest_var
                # print(f"{quest_id} is {self.is_green_quest_var}")
                self.is_green_quest_var = None
                return output
            else:
                await self.sleep(100)
        return False

    @check_alive
    async def is_completed_before(self, quest_id: int) -> bool:
        await self.turn_in_quest(quest_id)
        while(self.is_still_connected()):
            if self.is_completed_before_var is not None:
                output = self.is_completed_before_var
                # print(f"{quest_id} is {self.is_green_quest_var}")
                self.is_completed_before_var = None
                return output
            else:
                await self.sleep(100)
        return False

    @check_alive
    async def accept_quest_bulk(self, quest_id: int, increment: int, ensure:bool = False):
        print(f"accepting quest from {quest_id} to {quest_id + increment}")
        for i in range(increment):
            if ensure:
                await self.ensure_accept_quest(quest_id + i)
            elif not ensure:
                await self.accept_quest(quest_id + i)

    @check_alive
    async def register_quest(self, questId: int):
        if questId not in self.bot.registered_auto_quest_ids:
            self.bot.registered_auto_quest_ids.append(questId)
            await self.ensure_accept_quest(questId)
