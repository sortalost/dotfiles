@echo off
cls
doskey home=cd %USERPROFILE%
doskey cap=cd %USERPROFILE%\\Desktop\\yard\\cv2 ^&^& python nn.py $1 $2 $3 ^&^& cd %USERPROFILE%
doskey welp=echo i will do something about welp. Welp!
doskey sf = cd %USERPROFILE%\Desktop\play\Street_Fighter_2_Turbo ^&^& StreetFighter2Turbo.bat
doskey ascii = python dotfiles/ascii.py
doskey np = notepad $1
title %date%
echo #==================================================================^>^>
python dotfiles/ascii.py
echo #------------------------[ %date% ]-----------------------------
