@echo off
cls
doskey home=cd %USERPROFILE%
doskey welp=echo ascii, wiki, sf, np, cat, nws, song
doskey sf = cd %USERPROFILE%\Desktop\play\Street_Fighter_2_Turbo ^&^& StreetFighter2Turbo.bat
doskey ascii = python %USERPROFILE%\dotfiles\ascii.py
doskey wiki = python %USERPROFILE%\dotfiles\wiki.py $1 $2 $3 $4 $5 $6 $7 $8
doskey song = python %USERPROFILE%\dotfiles\song.py $1 $2 $3 $4 $5 $6 $7 $8
doskey nws = python %USERPROFILE%\dotfiles\misc.py newsletter
doskey cat = python %USERPROFILE%\dotfiles\misc.py cat $1 $2 $3 $4
doskey np = notepad $1
title %date%
echo #==================================================================^>^>
python %USERPROFILE%\dotfiles\ascii.py
echo #-------------------------[ %date% ]-------------------------------