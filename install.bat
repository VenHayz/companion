@ECHO off
CLS

ECHO Please go download Python 3.6 from https://www.python.org/ if you haven't already, before continuing.
PAUSE

python -m pip install -U discord.py[voice]

CLS
ECHO Installation complete! Have fun.
SET /p launch=Do you want to start the bot now? (Y/n) 

IF "%launch%"=="Y" (
    GOTO YES
)
IF "%launch%"=="y" (
    GOTO YES
)
IF "%launch%"=="" (
    GOTO YES
) ELSE (
    EXIT
)

:YES
.\run.bat
EXIT