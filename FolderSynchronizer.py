import os
import shutil
import time
import argparse
from datetime import datetime

def synchronize_folders(source_path, replica_path, log_file_path, interval):

    if not os.path.exists(source_path):
        print(f"Error: Source folder '{source_path}' not found.")
        return

    if not os.path.exists(replica_path):
        os.makedirs(replica_path)

    while True:
        try:

            sync_folders(source_path, replica_path, log_file_path)


            log_sync_time(log_file_path)


            time.sleep(interval)
        except KeyboardInterrupt:
            print("Synchronization stopped by user.")
            break

def sync_folders(source, replica, log_file):
    with open(log_file, 'a') as log:
        log.write(f"\n\nSynchronization at {datetime.now()}:\n")


        for root, dirs, files in os.walk(source):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(replica, os.path.relpath(source_file_path, source))


                shutil.copy2(source_file_path, replica_file_path)


                log.write(f"  Copied/Updated: {os.path.relpath(source_file_path, source)}\n")


        for root, dirs, files in os.walk(replica):
            for file in files:
                replica_file_path = os.path.join(root, file)
                source_file_path = os.path.join(source, os.path.relpath(replica_file_path, replica))

                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log.write(f"  Removed: {os.path.relpath(replica_file_path, replica)}\n")

def log_sync_time(log_file):
    with open(log_file, 'a') as log:
        log.write(f"\nSynchronization completed at {datetime.now()}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log", help="Path to the log file")

    args = parser.parse_args()

    synchronize_folders(args.source, args.replica, args.log, args.interval)
