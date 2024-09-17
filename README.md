# OBS Window Tracking Tool

This tool provides dynamic window tracking and zooming functionality for OBS (Open Broadcaster Software) on macOS. It allows you to automatically crop and scale the captured window based on mouse position and user-defined settings.

## Features

- Automatic window tracking and zooming
- Support for multiple applications with customizable settings
- Two modes: Scale and Center
- Keyboard shortcuts for quick mode switching
- Smooth animations for position changes

## Requirements

- macOS
- OBS Studio with obs-websocket plugin
- Python 3.7+
- PyAutoGUI
- simpleobsws
- pynput

## Installation

1. Clone this repository or download the source code.
2. Install the required Python packages:

```bash
pip install pyautogui simpleobsws pynput
```

3. Configure OBS:
   - Install the obs-websocket plugin if not already installed.
   - Set up a WebSocket server in OBS (Tools > WebSocket Server Settings).
   - Create a "macOS Screen Capture" source in your OBS scene.

4. Update the `config.py` file with your OBS WebSocket settings:

```python
host = "your_obs_ip"
port = your_obs_port
password = "your_obs_websocket_password"
obs_source = "macOS Screen Capture 2"
```

## Usage

1. Run the main script:

```bash
python main.py
```

2. The tool will start tracking the active window and adjusting the OBS source accordingly.

3. Use the following keyboard shortcuts:
   - `Ctrl + Shift + W`: Toggle between center and top window positioning
   - `Ctrl + Shift + S`: Switch between scale and center modes

4. To stop the script, press `Ctrl + C` in the terminal.

## Configuration

You can customize settings for different applications in the `app_config.py` file. Adjust parameters like scale, thresholds, and offsets to fine-tune the behavior for each application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
