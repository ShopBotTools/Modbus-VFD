This program is written for windows
It controls a Lenze VFD using modbus network protocol

Hoping to automate these steps later (maybe with Makefile), but for now...

Build instructions:
- cd into project folder
- Create virtual environment:
> python -m venv .\venv
> .\venv\Scripts\activate
> pip install -r .\requirements.txt
- Copy all .py files from workpace directory to venv\Lib\site-packages
> pyinstaller --onefile --noconsole --icon=rpm.ico main.py
- Move dist\main.exe to workspace directory
- Delete the files that were moved into venv\Lib\site-packages

Executable should be good to go!