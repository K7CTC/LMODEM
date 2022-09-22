import time
from turtle import width
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.console import Console
from rich.table import Column



console = Console()

sent_block_count = 0

console.show_cursor(False)

def move_cursor(row, column):
    print(f'\033[{row};{column}H', end='')

console.clear()

#ui elements:
move_cursor(1,1)
console.print('File Name:')




text_column = TextColumn('Connecting...', width=12)
bar_column = BarColumn(bar_width=None)
time_elapsed_column = TimeElapsedColumn()
time_remaining_column = TimeRemainingColumn()





move_cursor(10,1)
with Progress(transient=True) as progress:
    task = progress.add_task('Connecting...', start=False)
    time.sleep(5)


move_cursor(1,12)
console.print('test_file.jpg')


move_cursor(10,3)
with Progress() as progress:
    task = progress.add_task('   Sending...', total=70)
    while not progress.finished:
        progress.update(task, completed=sent_block_count, description='Sending...')
        sent_block_count += 1
        time.sleep(.5)

console.show_cursor(True)