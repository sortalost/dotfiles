@echo off
cls
doskey home=cd %USERPROFILE%
doskey welp=echo ascii, wiki, ub, sf, np, song, nws, cat, speak
doskey sf = cd %USERPROFILE%\Desktop\play\Street_Fighter_2_Turbo ^&^& StreetFighter2Turbo.bat
doskey ascii = python %USERPROFILE%\f"{os.getenv('USERPROFILE')}\\dotfiles\\newsletter.json"\ascii.py
doskey wiki = python %USERPROFILE%\dotfiles\wiki.py $*
doskey ub = python %USERPROFILE%\dotfiles\urbandictionary.py $*
doskey song = python %USERPROFILE%\dotfiles\song.py $*
doskey nws = python %USERPROFILE%\dotfiles\misc.py newsletter
doskey cat = python %USERPROFILE%\dotfiles\misc.py cat $*
doskey speak = python %USERPROFILE%\dotfiles\misc.py speak $*
doskey np = notepad $*
title %date%
echo #==================================================================^>^>
python %USERPROFILE%\dotfiles\ascii.py
echo #-------------------------[ %date% ]-------------------------------
