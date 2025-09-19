import asyncio

from core.commands.base import _CommandBase, check_alive

class MapCommands(_CommandBase):
    """Map travel and positioning helpers."""

    @check_alive
    async def goto_player(self, player_name: str):
        await self.bot.ensure_leave_from_combat(always=True)
        self.bot.write_message(f"%xt%zm%cmd%1%goto%{player_name}%")
        await self.sleep(1000)

    @check_alive
    async def join_house(self, houseName: str, safeLeave: bool = True):
        self.stop_aggro()
        if self.bot.strMapName.lower() == houseName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)
        msg = f"%xt%zm%house%1%{houseName}%"
        self.bot.write_message(msg)

    @check_alive
    async def join_map(self, mapName: str, roomNumber: int = None, safeLeave: bool = True) -> None:
        self.stop_aggro()
        if self.bot.strMapName.lower() == mapName.lower():
            return
        self.bot.is_joining_map = True
        await self.leave_combat(safeLeave)

        if roomNumber != None:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{roomNumber}%"
        elif self.bot.roomNumber != None:
            roomNumber = self.bot.roomNumber
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}-{self.bot.roomNumber}%"
        else:
            msg = f"%xt%zm%cmd%1%tfer%{self.bot.player.USER}%{mapName}%"
        self.bot.write_message(msg)

    def is_not_in_map(self, mapName: str) -> bool:
        return mapName.lower() != self.bot.strMapName.lower()

    @check_alive
    async def jump_cell(self, cell: str, pad: str) -> None:
        if self.bot.player.CELL.lower() != cell.lower() or self.bot.player.PAD.lower() != pad.lower():
            self.bot.jump_cell(cell, pad)
            #print(f"jump cell: {cell} {pad}")
            await asyncio.sleep(1)

    def is_not_in_cell(self, cell: str) -> bool:
        return self.bot.player.CELL.lower() != cell.lower()

    @check_alive
    async def walk_to(self, X: int, Y: int, speed: int = 8):
        await self.bot.walk_to(X, Y, speed)
        await self.sleep(200)
