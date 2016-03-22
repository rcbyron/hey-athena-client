@ECHO OFF
COLOR 0A
TITLE PyPi Site Uploader

ECHO Uploading to PyPi Site...
CD ..
CALL python setup.py sdist upload
ECHO.
ECHO Upload complete!
CD tools
PAUSE