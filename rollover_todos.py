import sys
from pathlib import Path
from re import match
from datetime import date, timedelta
import os

# if there are spaces in any of the folder names, Templater splits the path into a list so grab all of the returned
# arguments after the first one and join them together
daily_notes_dir_parts = sys.argv[1:]
daily_notes_dir = " ".join(daily_notes_dir_parts)
cwd_abs = os.path.join(os.getcwd(), daily_notes_dir)
daily_notes_dir = Path(cwd_abs).parents[1]

unchecked = r"- \[ \]"
prev_note = []
open_todos = []


def get_suffix(day) -> str:
    """
    The current file name format I'm using for periodic notes includes a suffix after the day such as
    "Monday, August 22nd, 2022"
    :param day: the day as an integer.
    :return: the suffix for the given day. If it's the first of the month, "st" will be returned
    """
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return suffix


def migrate_todos():
    """
    Find the most recent daily note.

    Start by trying to find yesterday's file. If it doesn't exist, decrement the day by one and try to find that file.
    Keep trying until a file is found or after 100 attempts.
    """
    prev_day = date.today() - timedelta(days=1)
    i = 0
    while True:
        # To prevent infinite loop, break after 100 attempts
        if i == 100:
            break
        file_name = prev_day.strftime(f'%A, %B %-d{get_suffix(prev_day.day)}, %Y.md')
        prev_day_year = str(prev_day.year)
        prev_day_month = prev_day.strftime('%b')
        try:
            extract_fname = file_name.split('.')[0]
            file_path = os.path.join(daily_notes_dir, prev_day_year, prev_day_month, file_name)
            with open(file_path, 'r+') as f:
                lines = f.readlines()
                for line in lines:
                    if match(unchecked, line):
                        open_todos.append(line)
                    else:
                        prev_note.append(line)
                f.seek(0)
                for line in prev_note:
                    f.write(line)
                f.truncate()
            for todo in open_todos:
                print(todo[:-1])
            break

        except FileNotFoundError:
            # If file isn't found, decrease day by 1
            prev_day = prev_day - timedelta(days=1)
            i += 1


if __name__ == '__main__':
    migrate_todos()
