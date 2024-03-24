@echo off

REM Run slave servers
start cmd /k python src\server\slave.py 6001
start cmd /k python src\server\slave.py 6002
start cmd /k python src\server\slave.py 6003

REM Run language model server
start cmd /k python src\server\language_model.py 6060

REM Run master server
start cmd /k python src\server\master.py

exit
