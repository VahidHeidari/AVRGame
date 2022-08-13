@echo off

set ARCHIVE_NAME=PyAVREmu



REM Archive data
set WEEK_DAY=%date:~0,3%
set DAY=%date:~7,2%
set MOUNTH=%date:~4,2%
set YEAR=%date:~10,4%
set COMB_DATE=%YEAR%%MOUNTH%%DAY%-%WEEK_DAY%

REM Default parameters
set ARCHIVE_ALL=false
set FULL_ARCHIVE_NAME=%ARCHIVE_NAME%-%COMB_DATE%.tar.gz

REM Tar compressor exe
set TAR="C:\Program Files\Git\usr\bin\tar.exe"



%TAR% -cvzf %FULL_ARCHIVE_NAME% ^
*.bat 							^
*.py							^
3rdParty/uzem/*.cpp				^
3rdParty/uzem/*.gdb				^
3rdParty/uzem/*.h				^
3rdParty/uzem/*.sh				^
3rdParty/uzem/*.txt 			^
Docs/*.txt						^
UnitTests/*.py					^
Datasets

echo ------------------------------------
echo All directories archived.
echo ------------------------------------

