import sqlite3
import datetime


def connect():
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS routine (
            Id INTEGER PRIMARY KEY,
            date TEXT,
            time TEXT DEFAULT '',
            earnings INTEGER,
            exercise TEXT,
            study TEXT,
            diet TEXT,
            python TEXT DEFAULT ''
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            routine_id INTEGER,
            reminder_time TEXT,
            message TEXT,
            is_active INTEGER DEFAULT 1,
            reminded INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute("PRAGMA table_info(routine)")
    columns = [column[1] for column in cur.fetchall()]
    expected = ['Id', 'date', 'time', 'earnings', 'exercise', 'study', 'diet', 'python']

    if columns != expected:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='routine'")
        if cur.fetchone():
            cur.execute("ALTER TABLE routine RENAME TO routine_legacy")
            cur.execute(
                """
                CREATE TABLE routine (
                    Id INTEGER PRIMARY KEY,
                    date TEXT,
                    time TEXT DEFAULT '',
                    earnings INTEGER,
                    exercise TEXT,
                    study TEXT,
                    diet TEXT,
                    python TEXT DEFAULT ''
                )
                """
            )
            cur.execute(
                """
                INSERT INTO routine (Id, date, time, earnings, exercise, study, diet, python)
                SELECT Id, date, '', earnings, exercise, study, diet, python
                FROM routine_legacy
                """
            )
            cur.execute("DROP TABLE routine_legacy")

    conn.commit()
    conn.close()


def insert(date, time='', earnings='', exercise='', study='', diet='', python_field=''):
    if date is None or str(date).strip() == '':
        raise ValueError('Date is required')

    if earnings in ('', None):
        earnings = 0

    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO routine (date, time, earnings, exercise, study, diet, python) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            str(date).strip(),
            str(time).strip() if time else '',
            int(earnings),
            str(exercise).strip() if exercise else '',
            str(study).strip() if study else '',
            str(diet).strip() if diet else '',
            str(python_field).strip() if python_field else '',
        ),
    )

    routine_id = cur.lastrowid
    conn.commit()
    conn.close()
    return routine_id


def view():
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM routine ORDER BY Id DESC")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def delete(id):
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM routine WHERE id=?", (id,))
    cur.execute("DELETE FROM reminders WHERE routine_id=?", (id,))
    conn.commit()
    conn.close()


def search(date='', time='', earnings='', exercise='', study='', diet='', python_field=''):
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()

    query = "SELECT * FROM routine WHERE 1=1"
    params = []

    if date and str(date).strip():
        query += " AND date=?"
        params.append(str(date).strip())

    if time and str(time).strip():
        query += " AND time=?"
        params.append(str(time).strip())

    if earnings not in ('', None):
        query += " AND earnings=?"
        params.append(int(earnings))

    if exercise and str(exercise).strip():
        query += " AND exercise=?"
        params.append(str(exercise).strip())

    if study and str(study).strip():
        query += " AND study=?"
        params.append(str(study).strip())

    if diet and str(diet).strip():
        query += " AND diet=?"
        params.append(str(diet).strip())

    if python_field and str(python_field).strip():
        query += " AND python=?"
        params.append(str(python_field).strip())

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


def add_reminder(routine_id, reminder_datetime, message='Routine reminder'):
    if not routine_id or not reminder_datetime:
        return

    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reminders (routine_id, reminder_time, message, is_active, reminded) VALUES (?, ?, ?, 1, 0)",
        (routine_id, reminder_datetime, message),
    )
    conn.commit()
    conn.close()


def get_due_reminders():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, routine_id, reminder_time, message FROM reminders WHERE is_active=1 AND reminded=0 AND reminder_time <= ? ORDER BY reminder_time ASC",
        (now,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_reminded(reminder_id):
    conn = sqlite3.connect('routine.db')
    cur = conn.cursor()
    cur.execute("UPDATE reminders SET reminded=1 WHERE id=?", (reminder_id,))
    conn.commit()
    conn.close()


connect()
