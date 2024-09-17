# app_config.py

import re

APP_SETTINGS = {
    "phpstorm": {
        "settings": [{
            "y_offset": -70,
            "scale": 2.0,
            "crop_left": 0,
            "left_threshold": 0.1,
            "right_threshold": 0.11,
            "top_threshold": 0.05,
            "bottom_threshold": 0.9,
            "window_patterns": ["*"]  # Match any window name for phpstorm
        }]
    },
    "Google Chrome": {
        "settings": [
            {
                "y_offset": -75,
                "scale": 2.0,
                "crop_left": 0,
                "left_threshold": 0.2,
                "right_threshold": 0.21,
                "top_threshold": 0.2,
                "bottom_threshold": 0.8,
                "window_patterns": ["*ByteLaunch, Inc Mail*"]
            },
            {
                "y_offset": -75,
                "scale": 2.0,
                "crop_left": -100,
                "left_threshold": 0.1,
                "right_threshold": 0.11,
                "top_threshold": 0.2,
                "bottom_threshold": 0.8,
                "window_patterns": ["*ChatGPT*"]
            },
            {
                "y_offset": -75,
                "scale": 2.0,
                "crop_left": 50,
                "left_threshold": 0.2,
                "right_threshold": 0.8,
                "top_threshold": 0.2,
                "bottom_threshold": 0.8,
                "window_patterns": ["*"]
            }
        ]
    },
    "default": {
        "settings": [{
            "y_offset": -50,
            "scale": 2.0,
            "crop_left": 0,
            "left_threshold": 0.2,
            "right_threshold": 0.8,
            "top_threshold": 0.2,
            "bottom_threshold": 0.8,
            "window_patterns": ["*"]  # Match any window name for default settings
        }]
    }
}


def get_settings_for_window(app_name, window_name):
    app_settings = APP_SETTINGS.get(app_name, APP_SETTINGS["default"])

    for setting in app_settings["settings"]:
        for pattern in setting["window_patterns"]:
            regex_pattern = pattern.replace("*", ".*").lower()
            if re.match(regex_pattern, window_name.lower()):
                return setting


    print(f"✅👉app name is {app_name} and window name is {window_name}")
    # print app_settings["settings"][0] key name
    print(f"✅👉: {app_settings['settings'][0]['window_patterns'][0]}")

    # If no match found, return the first setting (or you could return the default)
    return app_settings["settings"][0]
