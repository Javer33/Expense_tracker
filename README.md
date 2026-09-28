# Pennywise — Expense Tracker

A beginner-friendly Python desktop application for recording and managing daily expenses.

## Features
- Add expenses with title, category, amount, date, and description
- View records in a table
- Edit and delete selected records
- Search by title, category, or date
- Dashboard totals and category breakdown
- Permanent storage using JSON

## Technologies
Python, Tkinter/ttk, JSON, lists, dictionaries, functions, CRUD, validation, exception handling.

## Requirements
Python 3.9+ recommended. Tkinter is included with most standard Windows Python installations. No third-party packages are required.

## Run
1. Open this folder in VS Code.
2. Open the terminal in this folder.
3. Run: `python main.py`

The program creates `expenses.json` when saving the first expense. If the file is missing at startup, the application starts with an empty list.

## Date format
Enter dates as `YYYY-MM-DD`, for example `2026-09-28`.

## Data safety
If the JSON file is malformed or unreadable, the application reports an error and does not replace the file automatically. Back up the file before attempting manual repair.
