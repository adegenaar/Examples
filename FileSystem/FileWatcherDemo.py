from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#pip install watchdog for these to work


import os
import json
import time

class MyHandler(FileSystemEventHandler):
    """
    Handles occurring events by copying the file(s) from the source to the destination.
    """
    def on_modified(self, event):
        if event.is_directory: return
        for filename in os.listdir(folder_to_track):
            src = folder_to_track + "/" + filename
            new_destination = folder_destination + "/" + filename
            os.rename(src, new_destination)
        
    def on_created(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_moved(self, event):
        pass


folder_to_track = "C:/Users/albert.w.degenaar/Desktop/Source"
folder_destination = "C:/Users/albert.w.degenaar/Desktop/Destination"
event_handler = MyHandler()
observer = Observer()
observer.setDaemon(True)
observer.schedule(event_handler, folder_to_track,  recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
    