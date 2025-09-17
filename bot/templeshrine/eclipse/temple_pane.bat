@echo off
title Temple Shrine Dungeon

set PROJECT_PATH="D:\Python\aqw-python"
set BOT_PATH=bot.templeshrine.eclipse.bot_temple
set USER_NAME=u
set PASSWORD=p

echo Starting Temple Shrine Dungeon bots in a 2x2 grid...

REM 1. Buka window dengan panel pertama (akan menjadi kiri atas)
wt --title "1L solstice_p1" --suppressApplicationTitle cmd /k "cd /d %PROJECT_PATH% && echo 1 | py -m %BOT_PATH%"

echo Waiting (3 secs) for lead account to be ready...
timeout /t 3 /nobreak >nul

REM 2. Buat sisa 3 panel dengan logika grid 2x2
wt -w 0 split-pane -V -s 0.5 --title "2 solstice_p2" cmd /k "cd /d %PROJECT_PATH% && echo 2 | py -m %BOT_PATH%" ; ^
         move-focus left ; ^
         split-pane -H -s 0.5 --title "3 midnight_p1" cmd /k "cd /d %PROJECT_PATH% && echo 3 | py -m %BOT_PATH%" ; ^
         move-focus up ; move-focus right ; ^
         split-pane -H -s 0.5 --title "4 midnight_p2" cmd /k "cd /d %PROJECT_PATH% && echo 4 | py -m %BOT_PATH%"
         
echo Temple Shrine Dungeon is running...