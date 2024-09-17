# auto_update.py

import os
import sys
import time
import subprocess

def get_python_files():
    return [f for f in os.listdir('.') if f.endswith('.py')]

def get_last_modified_times(files):
    return {f: os.path.getmtime(f) for f in files}

def run_script():
    process = subprocess.Popen([sys.executable, 'main.py'])
    return process

def main():
    python_files = get_python_files()
    last_modified_times = get_last_modified_times(python_files)
    process = run_script()

    try:
        while True:
            time.sleep(1)  # Check every second
            current_modified_times = get_last_modified_times(python_files)

            if current_modified_times != last_modified_times:
                changed_files = [f for f in python_files if current_modified_times[f] != last_modified_times[f]]
                print(f"Files changed: {', '.join(changed_files)}. Restarting...")
                process.terminate()
                process.wait()
                process = run_script()
                last_modified_times = current_modified_times
    except KeyboardInterrupt:
        print("Auto-updater stopped.")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
