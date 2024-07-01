@echo off
color 0a
echo Installing required packages...
pip install -r requirements.txt

echo Cleaning console...
cls

echo Starting Discord bot...
python bot.py
pause