@echo off
REM Batch script to run the three Python scripts in sequence

REM Activate virtual environment if needed (uncomment and edit the next line)
REM call venv\Scripts\activate.bat

REM Run find_and_copy_scripts.py
python find_and_copy_scripts.py
IF %ERRORLEVEL% NEQ 0 (
    echo Error running find_and_copy_scripts.py
    exit /b %ERRORLEVEL%
)

REM Run create_menu.py
python create_menu.py
IF %ERRORLEVEL% NEQ 0 (
    echo Error running create_menu.py
    exit /b %ERRORLEVEL%
)

REM Run update_readme.py
python update_readme.py
IF %ERRORLEVEL% NEQ 0 (
    echo Error running update_readme.py
    exit /b %ERRORLEVEL%
)

echo All scripts executed successfully.
