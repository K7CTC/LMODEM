from ctypes import alignment
from time import sleep
from tkinter import W
from turtle import width

from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn, TaskProgressColumn, TimeRemainingColumn

total_blocks = 92
blocks_sent = 0


bar_column = BarColumn(bar_width=None, table_column=Column(width=50))
task_progress_column = TaskProgressColumn(table_column=Column(width=25))
time_remaining_column = TimeRemainingColumn(table_column=Column(width=25))
progress = Progress(bar_column, task_progress_column, time_remaining_column)

with progress:
    task = progress.add_task('Connecting...', start=False)
    sleep(5)
    progress.start_task(task)
    while not progress.finished:
        progress.update(task, completed=blocks_sent)
        blocks_sent += 1
        sleep(0.25)

