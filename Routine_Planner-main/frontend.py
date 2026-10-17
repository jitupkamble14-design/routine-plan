import tkinter as tk
from tkinter import messagebox
import winsound
import backend

selected_row = ()
records = []


def normalize_row(row):
    if not row:
        return {}

    if len(row) >= 8:
        routine_id, date, time, earnings, exercise, study, diet, python_value = row[:8]
    elif len(row) == 7:
        routine_id, date, earnings, exercise, study, diet, python_value = row
        time = ''
    else:
        routine_id, date, time, earnings, exercise, study, diet = row + ('',) * (7 - len(row))
        python_value = ''

    return {
        'id': routine_id,
        'date': date,
        'time': time or '',
        'earnings': earnings,
        'exercise': exercise or '',
        'study': study or '',
        'diet': diet or '',
        'python': python_value or '',
    }


def format_row(row):
    data = normalize_row(row)
    if not data:
        return ''

    time_text = f" | Time: {data['time']}" if data['time'] else ''
    return (
        f"{data['date']} | ${data['earnings']} | "
        f"Exercise: {data['exercise'] or '-'} | "
        f"Study: {data['study'] or '-'} | "
        f"Diet: {data['diet'] or '-'}{time_text}"
    )


def refresh_list(rows):
    global records
    records = rows or []
    listbox.delete(0, tk.END)

    if not records:
        listbox.insert(tk.END, 'No routine records found.')
        return

    for row in records:
        listbox.insert(tk.END, format_row(row))


def clear_form():
    global selected_row
    selected_row = ()
    date_var.set('')
    time_var.set('')
    earnings_var.set('')
    exercise_var.set('')
    study_var.set('')
    diet_var.set('')
    reminder_time_var.set('')
    reminder_note_var.set('')

    try:
        listbox.selection_clear(0, tk.END)
    except tk.TclError:
        pass


def populate_form(row):
    global selected_row
    selected_row = row
    if not row:
        clear_form(); return

    data = normalize_row(row)
    date_var.set(data['date'])
    time_var.set(data['time'])
    earnings_var.set(data['earnings'])
    exercise_var.set(data['exercise'])
    study_var.set(data['study'])
    diet_var.set(data['diet'])
    reminder_time_var.set('')
    reminder_note_var.set('')


def get_selected_row(event=None):
    try:
        index = listbox.curselection()[0]
    except (IndexError, tk.TclError):
        return

    if index >= len(records):
        return

    populate_form(records[index])


def view_command():
    refresh_list(backend.view())


def add_command():
    date_value = date_var.get().strip()
    time_value = time_var.get().strip()
    earnings_value = earnings_var.get().strip()
    exercise_value = exercise_var.get().strip()
    study_value = study_var.get().strip()
    diet_value = diet_var.get().strip()
    reminder_time_value = reminder_time_var.get().strip()
    reminder_note_value = reminder_note_var.get().strip()

    if not date_value:
        messagebox.showwarning('Missing date', 'Please add a date before saving your routine.')
        return

    try:
        routine_id = backend.insert(date_value, time_value, earnings_value, exercise_value, study_value, diet_value)
    except ValueError:
        messagebox.showerror('Invalid input', 'Earnings must be a valid number.')
        return

    if reminder_time_value:
        reminder_datetime = f"{date_value} {reminder_time_value}"
        backend.add_reminder(routine_id, reminder_datetime, reminder_note_value or f'Routine reminder for {date_value}')

    refresh_list(backend.view())
    clear_form()
    messagebox.showinfo('Success', 'Routine saved successfully.')


def search_command():
    rows = backend.search(
        date_var.get(),
        time_var.get(),
        earnings_var.get(),
        exercise_var.get(),
        study_var.get(),
        diet_var.get(),
    )
    refresh_list(rows)


def delete_command():
    if not selected_row:
        messagebox.showwarning('No selection', 'Select a routine from the list before deleting it.')
        return

    backend.delete(selected_row[0])
    refresh_list(backend.view())
    clear_form()
    messagebox.showinfo('Deleted', 'Routine deleted successfully.')


def run_reminder_check():
    due = backend.get_due_reminders()
    for reminder_id, _, reminder_time, message in due:
        backend.mark_reminded(reminder_id)
        winsound.Beep(880, 450)
        winsound.Beep(660, 450)
        winsound.Beep(880, 650)
        messagebox.showinfo('Routine Reminder', f'{message or "Time to check your routine!"}\nScheduled: {reminder_time}')

    root.after(5000, run_reminder_check)


root = tk.Tk()
root.title('Routine Planner Premium')
root.geometry('1180x760')
root.minsize(1000, 620)
root.configure(bg='#0f172a')

main = tk.Frame(root, bg='#0f172a', padx=20, pady=20)
main.pack(fill='both', expand=True)

header = tk.Label(main, text='Routine Planner', bg='#0f172a', fg='#f8fafc', font=('Segoe UI', 26, 'bold'))
header.pack(anchor='w')

sub = tk.Label(main, text='Premium daily tracking with reminder alerts', bg='#0f172a', fg='#cbd5e1', font=('Segoe UI', 11))
sub.pack(anchor='w', pady=(2, 18))

content = tk.Frame(main, bg='#0f172a')
content.pack(fill='both', expand=True)

form_card = tk.Frame(content, bg='#111827', padx=18, pady=18, highlightbackground='#334155', highlightthickness=1)
form_card.pack(side='left', fill='y', padx=(0, 18))

inner_form = tk.Frame(form_card, bg='#111827')
inner_form.pack(fill='both')

fields = [
    ('Date', 0), ('Time', 1), ('Earnings', 2), ('Exercise', 3), ('Study', 4), ('Diet', 5), ('Reminder Time', 6), ('Reminder Note', 7)
]

for label_text, row_index in fields:
    label = tk.Label(inner_form, text=label_text, bg='#111827', fg='#e2e8f0', font=('Segoe UI', 10, 'bold'))
    label.grid(row=row_index, column=0, sticky='w', padx=(0, 12), pady=8)


def make_entry(var, row, width=32):
    entry = tk.Entry(inner_form, textvariable=var, width=width, bg='#0b1220', fg='#f8fafc', insertbackground='#f8fafc', relief='flat', highlightthickness=1, highlightbackground='#374151')
    entry.grid(row=row, column=1, sticky='ew', pady=8)
    return entry


date_var = tk.StringVar(); time_var = tk.StringVar(); earnings_var = tk.StringVar(); exercise_var = tk.StringVar(); study_var = tk.StringVar(); diet_var = tk.StringVar(); reminder_time_var = tk.StringVar(); reminder_note_var = tk.StringVar()

make_entry(date_var, 0)
make_entry(time_var, 1)
make_entry(earnings_var, 2)
make_entry(exercise_var, 3)
make_entry(study_var, 4)
make_entry(diet_var, 5)
make_entry(reminder_time_var, 6)
make_entry(reminder_note_var, 7, width=36)

button_row = tk.Frame(form_card, bg='#111827')
button_row.pack(fill='x', pady=(18, 0))

buttons = [
    ('Add Routine', '#7c3aed', add_command),
    ('Search', '#334155', search_command),
    ('Delete', '#dc2626', delete_command),
    ('View All', '#475569', view_command),
    ('Clear', '#64748b', clear_form),
]

for idx, (text, color, command) in enumerate(buttons):
    btn = tk.Button(button_row, text=text, bg=color, fg='white', activebackground=color, relief='flat', bd=0, padx=12, pady=9, font=('Segoe UI', 10, 'bold'), command=command)
    btn.grid(row=0, column=idx, padx=(0, 8), sticky='ew')

button_row.grid_columnconfigure(tuple(range(len(buttons))), weight=1)

list_card = tk.Frame(content, bg='#111827', padx=14, pady=14, highlightbackground='#334155', highlightthickness=1)
list_card.pack(side='right', fill='both', expand=True)

list_title = tk.Label(list_card, text='Routine Entries', bg='#111827', fg='#f8fafc', font=('Segoe UI', 12, 'bold'))
list_title.pack(anchor='w', pady=(0, 10))

listbox = tk.Listbox(
    list_card,
    bg='#0b1220',
    fg='#f8fafc',
    font=('Segoe UI', 10),
    height=18,
    width=60,
    highlightthickness=0,
    activestyle='none',
)
listbox.pack(fill='both', expand=True)

scroll = tk.Scrollbar(list_card, orient='vertical', command=listbox.yview)
scroll.pack(side='right', fill='y')
listbox.config(yscrollcommand=scroll.set)
listbox.bind('<<ListboxSelect>>', get_selected_row)

content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(1, weight=2)

refresh_list(backend.view())
root.after(5000, run_reminder_check)
root.mainloop()
