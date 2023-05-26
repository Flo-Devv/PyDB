''' This file contains the class for the asynchronous scheduler that will delete files after a certain amount of time. '''

from flask import Flask
import threading
import time
import os

class FileDeletionScheduler(threading.Thread):
    '''
    This class is a thread that will delete files after a certain amount of time.
    :param interval: The amount of time in seconds to wait before deleting a file.
    :param win: The Flask app.
    '''
    def __init__(self, interval=300, win: Flask = None):
        super().__init__()
        self.daemon = True
        self.win = win
        self.tasks = {}
        self.lock = threading.Lock()
        self.interval = interval
        print('File deletion scheduler initialized.')

    def run(self):
        while True:
            with self.lock:
                # if files in upload folder are not in the task list, delete them
                for file in os.listdir(self.win.config['UPLOAD_FOLDER']):
                    if file not in [filename for filename, _, _ in self.tasks.values()]:
                        os.remove(os.path.join(self.win.config['UPLOAD_FOLDER'], file))
                current_time = time.time()
                completed_tasks = []

                for task_id, (filename, timestamp, interval) in self.tasks.items():
                    if current_time - timestamp >= interval:
                        if os.path.exists(os.path.join(self.win.config['UPLOAD_FOLDER'], filename)):
                            os.remove(os.path.join(self.win.config['UPLOAD_FOLDER'], filename))
                        completed_tasks.append(task_id)
                # Remove completed tasks from the task list
                for task_id in completed_tasks:
                    del self.tasks[task_id]

            time.sleep(60)  # Check every minute

    def schedule_deletion(self, filename, interval=None):
        with self.lock:
            task_id = int(time.time() * 1000)  # Unique task ID based on current time
            timestamp = time.time()
            interval = interval or self.interval
            self.tasks[task_id] = (filename, timestamp, interval)

        return task_id