@echo off
cls
doskey home=cd %USERPROFILE%
doskey welp=echo ascii, wiki, sf, np
doskey sf = cd %USERPROFILE%\Desktop\play\Street_Fighter_2_Turbo ^&^& StreetFighter2Turbo.bat
doskey ascii = python %USERPROFILE%\dotfiles\ascii.py
doskey wiki = python %USERPROFILE%\dotfiles\wiki.py $1 $2 $3 $4 $5 $6 $7 $8
doskey np = notepad $1
title %date%
echo #==================================================================^>^>
python %USERPROFILE%\dotfiles\ascii.py
echo #-------------------------[ %date% ]-------------------------------
