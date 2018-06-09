SETLOCAL ENABLEDELAYEDEXPANSION
set FROMDIR=decompiled
FOR /R %FROMDIR% %%a in (*.pyo) DO (
	set newFile=%%~da%%~pa%%~nxa
	set newFile=!newFile:.pyo=.py!
	
	set oldFile=%%~da%%~pa%%~nxa
	
	echo "old: " + !oldFile!
	echo "new: " + !newFile!
	python "C:\Work\uncompyle-2.4-3.2.0\bin\uncompyle6" "!oldFile!" > "!newFile!"
)