@echo off
title Temple Shrine Dungeon

echo Starting Temple Shrine Dungeon bots in tabs...

set PROJECT_PATH="D:\Python\aqw-python"
set BOT_PATH=bot.templeshrine.ascendeclipse.bot_temple
set USER_NAME=u
set PASSWORD=p

wt new-tab --title "1L solstice_p1" cmd /k "cd /d %PROJECT_PATH% && echo 1 | py -m %BOT_PATH%"

echo Waiting (3 secs) for lead account to be ready...
timeout /t 3 /nobreak >nul

wt -w 0 new-tab --title "2 solstice_p2" cmd /k "cd /d %PROJECT_PATH% && echo 2 | py -m %BOT_PATH%" ; ^
   new-tab --title "3 midnight_p1" cmd /k "cd /d %PROJECT_PATH% && echo 3 | py -m %BOT_PATH%" ; ^
   new-tab --title "4 midnight_p2" cmd /k "cd /d %PROJECT_PATH% && echo 4 | py -m %BOT_PATH%"
   
echo Temple Shrine Dungeon is running...