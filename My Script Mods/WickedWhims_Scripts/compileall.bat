python -O -m compileall Scripts > compilelog.txt
pause
if exist ..\Wickedwhims_compiled\compiled del /y ..\Wickedwhims_compiled\compiled
SETLOCAL ENABLEDELAYEDEXPANSION
set FROMDIR=Scripts
set OUTPUTDIR=compiled
FOR /R %FROMDIR% %%a in (*.pyo) DO (
	set newFile=%%~da%%~pa
	set newFile=!newFile:Scripts=compiled!
	set newFile=!newFile:\__pycache__\=\!
	
	set oldFile=%%~a
	set oldFile=!oldFile:.cpython-33=!
	MOVE "%%a" "!oldFile!"
	echo "newfile: " + !newFile!
	echo "copying: "
	xcopy "!oldFile!" "!newFile!" /fys
	del "!oldFile!"
	echo "done copying"
)
FOR /R %FROMDIR% %%a in (__pycache__) DO (
	rmdir /S /Q "%%a\"
)
if exist "..\Wickedwhims_compiled\TURBODRIVER_WickedWhims_Scripts.ts4script" del /S "..\Wickedwhims_compiled\TURBODRIVER_WickedWhims_Scripts.ts4script"
7z.exe a -r -tzip "..\Wickedwhims_compiled\TURBODRIVER_WickedWhims_Scripts.ts4script" ".\..\Wickedwhims_compiled\compiled\*"