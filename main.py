# main.py

import asyncio
import pyautogui
from pynput import mouse
from obs_client import OBSClient
from window_info import get_active_window_info
from keyboard_handler import setup_keyboard_listener
from transform_handler import update_obs_crop_and_scale, update_obs_crop_and_center
from config import host, port, password, obs_source

async def main():
    obs_client = OBSClient(host, port, password)
    try:
        await obs_client.connect()
        print("Connected to OBS")
        await obs_client.wait_until_identified()
        print("Authenticated with OBS")

        canvas_size = await obs_client.get_canvas_size()
        if not canvas_size:
            return

        canvas_width, canvas_height = canvas_size
        current_scene = None
        source_id = None
        last_window = None

        keyboard_listener, keyboard_handler = setup_keyboard_listener(obs_client)
        keyboard_listener.start()

        mouse_click_queue = asyncio.Queue()

        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                mouse_click_queue.put_nowait(None)

        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

        async def handle_mouse_clicks():
            while True:
                await mouse_click_queue.get()
                await obs_client.handle_mouse_click()

        asyncio.create_task(handle_mouse_clicks())

        while True:
            try:
                app_name, window_name, x, y, width, height = get_active_window_info()
                mouse_x, mouse_y = pyautogui.position()

                current_window = f"{app_name} - {window_name}"
                print(f"")
                print(f"App: {app_name}, Window: {window_name}, Position: ({x}, {y}), Size: {width}x{height}")
                print(f"Mouse position: ({mouse_x}, {mouse_y})")

                if current_window != last_window or current_scene is None:
                    await obs_client.switch_window(current_window)
                    current_scene = await obs_client.get_current_scene()
                    source_id = await obs_client.get_source_id(current_scene, obs_source)
                    if source_id is None:
                        print(f"Could not find '{obs_source}' source")
                        return
                    last_window = current_window

                print(f"Current mode: {obs_client.current_mode}")
                print(f"Current window_position 🚀: {obs_client.window_position}")

                if obs_client.current_mode == "scale":
                    await update_obs_crop_and_scale(obs_client, x, y, width, height, mouse_x, mouse_y, canvas_width, canvas_height, current_scene, source_id, app_name)
                else:
                    await update_obs_crop_and_center(obs_client, x, y, width, height, mouse_x, mouse_y, canvas_width, canvas_height, current_scene, source_id, app_name)

                await asyncio.sleep(0.05)  # Update every 0.05 seconds for smoother movement
            except Exception as e:
                print(f"Error in main loop: {str(e)}")
                import traceback
                traceback.print_exc()
    except KeyboardInterrupt:
        print("Script stopped by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await obs_client.disconnect()
        print("Disconnected from OBS")
        keyboard_listener.stop()
        mouse_listener.stop()

if __name__ == "__main__":
    asyncio.run(main())
