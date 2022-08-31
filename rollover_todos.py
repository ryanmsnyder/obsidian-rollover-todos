import sys
from pathlib import Path
from re import match
from datetime import datetime, date, timedelta
import os

# if there are spaces in any of the folder names, Templater splits the path into a list so grab all the returned
# arguments after the first one and join them together
daily_notes_dir_parts = sys.argv[1:]
new_note_abs_path = " ".join(daily_notes_dir_parts)  # TODO: what happens if you join a list of 1 items with a space
daily_notes_dir = Path(new_note_abs_path).parents[2]
new_note_fname = os.path.basename(new_note_abs_path)

# regex patterns
unchecked = "\\s*- \\[ \\] [^\n ]"
bullet_point = "\\s+-[ \t]+(?!\\[ \\])[^\n ]"
empty_todo = "\\s*- \\[ \\](|[\n ]+)$"
empty_bullet = "\\s*-(|[\n ]+)$"

prev_note = []
open_todos = []


def get_new_note_date():
    # Remove day suffix to convert to datetime object (i.e. 30th will become 30)
    split_date = new_note_fname[:-3].split(',')
    remove_suffix = split_date[1][0:-2]
    split_date[1] = remove_suffix
    new_note_date_str = ','.join(split_date)
    new_note_date = datetime.strptime(new_note_date_str, '%A, %B %d, %Y')
    return new_note_date


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

    Start by trying to find the prior day's file (starting from the target note's date). If it doesn't exist, decrement
    the day by one and try to find that file. Keep trying until a file is found or after 100 attempts.
    """
    prev_day = get_new_note_date() - timedelta(days=1)
    i = 0
    while True:
        # To prevent infinite loop, break after 100 attempts
        if i == 100:
            break
        file_name = prev_day.strftime(f'%A, %B %-d{get_suffix(prev_day.day)}, %Y.md')
        prev_day_year = str(prev_day.year)
        prev_day_month = prev_day.strftime('%b')
        try:
            file_path = os.path.join(daily_notes_dir, prev_day_year, prev_day_month, file_name)
            # file_path = r"/Users/ryan.snyder/Desktop/todo.md"
            with open(file_path, 'r+') as f:
                lines = f.readlines()
                prev_item_todo = False
                for line in lines:
                    if prev_item_todo:
                        # Also grab any bullet points that are nested under the todo item
                        if match(bullet_point, line):
                            open_todos.append(line)
                            continue
                    if match(unchecked, line):
                        open_todos.append(line)
                        prev_item_todo = True
                    else:
                        # if it's an empty bullet point or empty TODO, don't write it back to previous note
                        if not match(empty_todo, line) and not match(empty_bullet, line):
                            prev_note.append(line)
                            prev_item_todo = False

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
