import time
import rich.progress 

total_blocks = 30
requested_blocks = 30
received_blocks = 0

progress = rich.progress.Progress(rich.progress.BarColumn(bar_width=59),
                                    rich.progress.TaskProgressColumn(),
                                    rich.progress.TimeRemainingColumn(),
                                    rich.progress.TimeElapsedColumn())
task = progress.add_task('Receiving Blocks...',total=total_blocks)

with progress:
    while True:
        
        progress.update(task, completed=received_blocks)
        time.sleep(0.0)

        received_blocks += 1
        
        progress.update(task, completed=received_blocks)
        time.sleep(.5)
        
        if received_blocks == total_blocks:
            break