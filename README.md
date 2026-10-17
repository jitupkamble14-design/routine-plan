# Routine Planner

A lightweight desktop application for tracking daily routines, habits, earnings, and reminders. It is built in Python using Tkinter and SQLite, making it easy to manage personal tasks from a simple GUI without needing a web server.

## Overview

Routine Planner helps users record daily details such as:
- date and time
- earnings
- exercise
- study progress
- diet information
- reminder notifications

The app stores all records in a local SQLite database and provides a simple interface to add, search, view, and delete entries.

## Features

- Add daily routine entries
- Track earnings for each day
- Record exercise, study, and diet information
- Search records by date or category
- View all saved routine entries
- Delete old or incorrect records
- Set reminder alerts for scheduled tasks
- Store data locally in SQLite

## Tech Stack

- Python 3
- Tkinter (GUI)
- SQLite (local database)
- Windows `winsound` for reminder alerts

## Project Structure

```text
routine-plan/
├── README.md
├── Routine_Planner-main/
│   ├── backend.py        # SQLite database logic and reminder functions
│   ├── frontend.py       # Tkinter user interface
│   ├── routine.db        # Local database file
│   ├── routine.py        # SQLite database file used by the app
│   └── __pycache__/      # Python cache files
└── .gitignore
```

## Installation

1. Make sure Python 3 is installed on your system.
2. Clone the repository:

```bash
git clone https://github.com/jitupkamble14-design/routine-plan.git
cd routine-plan
```

3. Open the app folder:

```bash
cd Routine_Planner-main
```

4. Run the application:

```bash
python frontend.py
```

Note: This project uses Tkinter, which is included with most Python installations. On Windows, `winsound` is available for the reminder beep notifications.

## Usage

1. Enter the date, time, earnings, exercise, study, and diet details.
2. Optionally add a reminder time and reminder note.
3. Click `Add Routine` to save the record.
4. Use `Search` to filter entries.
5. Click any row in the list to select it, then choose `Delete` if needed.
6. Click `View All` to display all stored routines.

## Database

The app uses SQLite to store routine data locally in `routine.db`.

Example fields stored in each record:
- `Id`
- `date`
- `time`
- `earnings`
- `exercise`
- `study`
- `diet`
- `python`

## Reminder Functionality

The app allows users to add reminder notifications for a scheduled routine. When the reminder time is reached, it plays a sound and shows a popup message.

## Requirements

- Python 3.8+
- Tkinter
- SQLite support
- Windows environment for full reminder compatibility

## License

No license file is currently included in the repository. If this project will be shared publicly, add a license such as MIT or Apache 2.0 before release.

## Contact

Project maintained by: jitupkamble14-design

For questions or improvements, open an issue in this repository.
