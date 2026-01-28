@echo off
chcp 65001 > nul
cd /d D:\repository\news-crawler-mcp
call venv\Scripts\activate.bat
python run_scheduler.py
