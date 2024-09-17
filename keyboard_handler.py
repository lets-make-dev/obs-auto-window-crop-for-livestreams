# keyboard_handler.py

from pynput import keyboard

class KeyboardHandler:
    def __init__(self, obs_client):
        self.obs_client = obs_client
        self.current_mode = "scale"
        self.window_position = "center"
        self.ctrl_pressed = False
        self.option_pressed = False
        self.cmd_pressed = False
        self.shift_pressed = False

    def on_press(self, key):
        if key == keyboard.Key.ctrl:
            self.ctrl_pressed = True
        elif key == keyboard.Key.alt:
            self.option_pressed = True
        elif key == keyboard.Key.cmd:
            self.cmd_pressed = True
        elif key == keyboard.Key.shift:
            self.shift_pressed = True

        try:

            if key.char == 'w' and self.ctrl_pressed and self.shift_pressed:
                print(f"   ❗ Current window_position:")
                self.window_position = "top" if self.window_position == "center" else "center"
                self.obs_client.window_position = self.window_position
                print(f"Switched window position to {self.window_position}")

            if key.char == 's' and self.ctrl_pressed and self.shift_pressed:
                print(f"   ❗„„ Current current_mode: {self.current_mode}")
                self.current_mode = "center" if self.current_mode == "scale" else "scale"
                self.obs_client.current_mode = self.current_mode
                print(f"Switched to {self.current_mode} mode")

        except AttributeError:
            pass

    def on_release(self, key):
        if key == keyboard.Key.ctrl:
            self.ctrl_pressed = False
        elif key == keyboard.Key.alt:
            self.option_pressed = False
        elif key == keyboard.Key.cmd:
            self.cmd_pressed = False
        elif key == keyboard.Key.shift:
            self.shift_pressed = False

def setup_keyboard_listener(obs_client):
    handler = KeyboardHandler(obs_client)
    return keyboard.Listener(on_press=handler.on_press, on_release=handler.on_release), handler
