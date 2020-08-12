@echo off

cd %~dp0

set INPUT=%1
set OUTPUT=%~dp1

python test.py -- %INPUT% %OUTPUT%

@pause