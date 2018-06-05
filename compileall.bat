python -O -m compileall decompiled > compilelog.txt
if exist compiled del /y compiled
SETLOCAL ENABLEDELAYEDEXPANSION
set FROMDIR=decompiled
set OUTPUTDIR=compiled
FOR /R %FROMDIR% %%a in (*.pyo) DO (
	set newFile=%%~da%%~pa
	set newFile=!newFile:decompiled=compiled!
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
if exist "compiled\TURBODRIVER_WickedWhims_Scripts.ts4script" del /S "compiled\TURBODRIVER_WickedWhims_Scripts.ts4script"
7z.exe a -r -tzip "compiled\TURBODRIVER_WickedWhims_Scripts.ts4script" ".\compiled\*"