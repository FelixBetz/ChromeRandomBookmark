@echo off  

for /f "tokens=*" %%i in ('dir /s/b *.py') DO  call :concat %%i 

python -m pylint %myvar%
exit

:concat  
set myvar=%myvar%%1     

