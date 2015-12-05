@echo OFF
echo Downloading latest spritedata...
powershell -Command "Invoke-WebRequest http://rhcafe.us.to/spritexml.php -OutFile reggiedata/spritedata.xml"
echo Done!
echo Starting Reggie!
cmd /k C:/Python34/python.exe reggie.py
@echo ON