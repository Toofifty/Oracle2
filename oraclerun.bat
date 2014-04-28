@echo OFF
cd oracle
:LOOP
python bot.py --pass wombat1 --channel #rapid
pause>nul
goto LOOP