# window_info.py

import subprocess
import re

def get_active_window_info():
    script = '''
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        set frontAppName to name of first application process whose frontmost is true
        tell process frontApp
            set windowName to name of front window
            set windowPosition to position of front window
            set windowSize to size of front window
        end tell
        return {frontAppName, windowName, item 1 of windowPosition, item 2 of windowPosition, item 1 of windowSize, item 2 of windowSize}
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    output = result.stdout.strip()

    # Use a more flexible regex pattern
    match = re.match(r'(.+?), (.*), (-?\d+), (-?\d+), (\d+), (\d+)$', output)

    if match:
        app_name = match.group(1)
        window_name = match.group(2)
        x, y, width, height = map(int, match.group(3, 4, 5, 6))
        return app_name, window_name, x, y, width, height
    else:
        # If the regex doesn't match, try a fallback parsing method
        parts = output.rsplit(', ', 4)
        if len(parts) == 5:
            app_and_window = parts[0].split(', ', 1)
            if len(app_and_window) == 2:
                app_name, window_name = app_and_window
                try:
                    x, y, width, height = map(int, parts[1:])
                    return app_name, window_name, x, y, width, height
                except ValueError:
                    pass  # If we can't convert to int, we'll raise the ValueError below

    raise ValueError(f"Failed to parse AppleScript output: {output}")
