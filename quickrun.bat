@echo OFF
cd oracle
:LOOP
python bot.py --nick Oracle_ --verbose --channel #rapid
pause>nul
goto LOOP