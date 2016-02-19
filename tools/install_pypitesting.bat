@ECHO OFF
COLOR 0A
TITLE PyPi Testing Site Installer

ECHO Installing from PyPi Testing Site...
CALL pip install -i https://testpypi.python.org/pypi HeyAthena
ECHO.
ECHO Install complete!
PAUSE