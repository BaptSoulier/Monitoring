import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import threading
import json
from config.app_config import Config
from core.log_manager import log_info, log_warning, log_error

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, watched_files):
        super().__init__()
        self.watched_files = watched_files

    def on_modified(self, event):
        if not event.is_directory and event.src_path in self.watched_files:
            log_info(f"Fichier modifié : {event.src_path}", event.src_path)

    def on_created(self, event):
        if not event.is_directory and event.src_path in self.watched_files:
            log_info(f"Fichier créé : {event.src_path}", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and event.src_path in self.watched_files:
            log_warning(f"Fichier supprimé : {event.src_path}", event.src_path)

    def on_moved(self, event):
        if not event.is_directory and (event.src_path in self.watched_files or event.dest_path in self.watched_files):
            log_info(f"Fichier déplacé de {event.src_path} à {event.dest_path}", event.src_path)

def start_monitoring(paths, watched_files):
    event_handler = FileChangeHandler(watched_files)
    observer = Observer()
    for path in paths:
        observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def run_watcher_in_thread(paths, watched_files):
    thread = threading.Thread(target=start_monitoring, args=(paths, watched_files))
    thread.daemon = True
    thread.start()

def load_watched_files():
    try:
        with open(Config.WATCHED_FILES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_watched_files(watched_files):
    with open(Config.WATCHED_FILES_FILE, 'w') as f:
        json.dump(watched_files, f)

if __name__ == "__main__":
    logging.basicConfig(filename=Config.LOG_FILE, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    from webapp import app
    with app.app_context():
        from database.db import init_db
        init_db(app)
        watched_files = load_watched_files()
        if watched_files:
            run_watcher_in_thread(watched_files, watched_files)
        time.sleep(60)
