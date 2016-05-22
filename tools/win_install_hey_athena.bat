@ECHO OFF
COLOR 0A
TITLE Hey Athena - Windows Batch Installer

SET orig_dir=%CD%
SET temp_dir=C:\AthenaTemp
SET avbin_url="https://github.com/downloads/AVbin/AVbin/AVbin10-win32.exe"
SET success=0

ECHO Running "Hey Athena" installer...
ECHO.

REM Check if python is in path
WHERE python > nul
IF %ERRORLEVEL% NEQ 0 (
	ECHO ERROR: "python" wasn't found in the environment variable path.\n
	GOTO :TERMINATE
)

REM Detect python version/bit size
SET get_version=python -c "import sys, re; m = re.match('(\d\.\d).*', sys.version); print(m.group(1))"
SET get_bit=python -c "import sys; print('64-bit') if sys.maxsize > 2**32 else print('32-bit')"
FOR /F %%i IN (' %get_version% ') DO SET p_version=%%i
FOR /F %%i IN (' %get_bit% ') DO SET p_bit=%%i

ECHO Detected Python %p_version% (%p_bit%)
ECHO.
IF NOT "%p_version%" == "3.4" (
	IF NOT "%p_version%" == "3.5" (
		ECHO ERROR: This installer requires python version 3.4 and above.
		GOTO :TERMINATE
	)
)
IF NOT "%p_bit%" == "32-bit" (
	IF NOT "%p_bit%" == "64-bit" (
		ECHO ERROR: The python bit size could not be determined.
		GOTO :TERMINATE
	)
)

REM Begin install
ECHO Creating install directory: %temp_dir%
ECHO.
MKDIR %temp_dir%
CD %temp_dir%

REM AVBin download
ECHO Downloading AVBin...
CALL bitsadmin.exe /transfer "Hey Athena AVBin" /priority FOREGROUND %avbin_url% "%temp_dir%\avbin.exe" >> avbin-log.txt

REM Pocketsphinx download
ECHO Downloading Pocketsphinx (pre-compiled)...
IF "%p_bit%" == "32-bit" SET bit_ext=win32.whl
IF "%p_bit%" == "64-bit" SET bit_ext=win_amd64.whl
IF "%p_version%" == "3.4" SET ps_file=pocketsphinx-0.0.9-cp34-cp34m-%bit_ext%
IF "%p_version%" == "3.5" SET ps_file=pocketsphinx-0.0.9-cp35-cp35m-%bit_ext%
CALL bitsadmin.exe /transfer "Hey Athena Pocketsphinx" /priority FOREGROUND "http://heyathena.com/assets/pocketsphinx/%ps_file%" "%temp_dir%\%ps_file%" >> pocketsphinx-log.txt

REM AVBin install
ECHO Installing AVBin...
CALL avbin.exe
REM Fix avbin install error
IF EXIST "C:\Windows\System32\avbin.dll"   MOVE "C:\Windows\System32\avbin.dll"   "C:\Windows\SysWOW64\avbin.dll"
IF EXIST "C:\Windows\System32\avbin64.dll" MOVE "C:\Windows\System32\avbin64.dll" "C:\Windows\SysWOW64\avbin64.dll"
IF %ERRORLEVEL% NEQ 0 (
	ECHO.
	ECHO ERROR: AVBin files could not be moved. Please run as administrator.
	ECHO.
	GOTO :TERMINATE
)

REM Pocketsphinx install
ECHO Installing Pocketsphinx...
CALL pip3 install --upgrade "%temp_dir%\%ps_file%"

REM Hey Athena install
ECHO Installing Hey Athena...
CALL pip3 install --upgrade HeyAthena

IF %ERRORLEVEL% EQU 0 (
	ECHO Installation successful!
	SET success=1
)

:TERMINATE
CD %orig_dir%
ECHO Removing installation files: %temp_dir%
RD /S /Q %temp_dir%
IF %success% EQU 0 GOTO :END

:RUN
CHOICE /M "Would you like to run Hey Athena now?"
IF %ERRORLEVEL% EQU 1 (
	ECHO.
	ECHO Running Hey Athena...
	PAUSE
	ECHO.
	CALL python -m athena.__main__
)

:END
ECHO.
ECHO Terminating...
ECHO.
PAUSE
EXIT /b
