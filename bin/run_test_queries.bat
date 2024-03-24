@echo off
REM Run multi_client.py script with Python 3.12 on Windows

REM Change directory to the location of multi_client.py script
cd /d "%~dp0..\src\client"

REM Run the Python script with the appropriate command
python multi_client.py ..\data\test_queries.csv 4
