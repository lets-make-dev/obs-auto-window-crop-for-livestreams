# transform_handler.py

import pyautogui
from app_config import APP_SETTINGS
import asyncio
from window_info import get_active_window_info
from app_config import get_settings_for_window
import time
from config import obs_source  # Import the obs_source from config.py

# At the top of the file, after imports
current_position = {"x": 0, "y": 0}

# This function will fit the window within the canvas height and center it horizontally
async def update_obs_crop_and_scale(obs_client, x, y, width, height, mouse_x, mouse_y, canvas_width, canvas_height, current_scene, source_id, app_name):
    try:
        screen_width, screen_height = pyautogui.size()
        scale = 2.0

        crop_left = x * scale
        crop_top = y * scale
        crop_right = (screen_width - (x + width)) * scale
        crop_bottom = (screen_height - (y + height)) * scale

        crop_success = await obs_client.set_source_filter_settings(obs_source, "Crop/Pad", {
            "left": crop_left,
            "top": crop_top,
            "right": crop_right,
            "bottom": crop_bottom
        })

        if crop_success:
            print("Crop updated successfully")
        else:
            print("Failed to update crop")

        scaled_width = width * scale
        scaled_height = height * scale

        # Calculate the maximum scale that allows the window to fit within the canvas height minus 100px
        max_height = canvas_height - 50  # Subtracting 100px from the top
        scale_x = canvas_width / scaled_width
        scale_y = max_height / scaled_height
        fit_scale = min(scale_x, scale_y)

        final_width = scaled_width * fit_scale
        final_height = scaled_height * fit_scale

        # Position the window 100px from the top
        center_x = (canvas_width - final_width) / 2
        top_y = 50  # 100px from the top

        transform_success = await obs_client.set_scene_item_transform(current_scene, source_id, {
            "positionX": center_x,
            "positionY": top_y,
            "scaleX": fit_scale,
            "scaleY": fit_scale
        })

        if transform_success:
            print(f"Transform updated successfully: pos({center_x}, {top_y}), scale({fit_scale})")
        else:
            print("Failed to update transform")

    except Exception as e:
        print(f"Error in update_obs_crop_and_scale: {str(e)}")
        import traceback
        traceback.print_exc()

async def animate_transform(obs_client, current_scene, source_id, start_x, start_y, target_x, target_y, scale, duration=0.3):
    global current_position

    # Check if 1 seconds have passed since the last click
    if time.time() - obs_client.last_click_time < 1:
        # If less than 5 seconds have passed, just set the final position without animation
        transform_success = await obs_client.set_scene_item_transform(current_scene, source_id, {
            "positionX": target_x,
            "positionY": target_y,
            "scaleX": scale,
            "scaleY": scale
        })
        if transform_success:
            current_position["x"] = target_x
            current_position["y"] = target_y
        return

    steps = 30
    step_duration = duration / steps

    for i in range(steps + 1):
        progress = i / steps
        current_x = start_x + (target_x - start_x) * progress
        current_y = start_y + (target_y - start_y) * progress

        transform_success = await obs_client.set_scene_item_transform(current_scene, source_id, {
            "positionX": current_x,
            "positionY": current_y,
            "scaleX": scale,
            "scaleY": scale
        })

        if transform_success:
            current_position["x"] = current_x
            current_position["y"] = current_y

        await asyncio.sleep(step_duration)

async def update_obs_crop_and_center(obs_client, x, y, width, height, mouse_x, mouse_y, canvas_width, canvas_height, current_scene, source_id, app_name):
    global current_position
    try:
        app_name, window_name, x, y, screen_width, screen_height = get_active_window_info()

        app_settings = get_settings_for_window(app_name, window_name)

        scale = app_settings['scale']
        left_threshold = app_settings['left_threshold']
        right_threshold = app_settings['right_threshold']
        top_threshold = app_settings['top_threshold']
        bottom_threshold = app_settings['bottom_threshold']

        if obs_client.window_position == "center":
            center_y = (canvas_height - height * scale) / 2
        else:  # "top"
            center_y = app_settings["y_offset"]

        print(f"👉👉App: {app_name}, {obs_client.window_position} Position: ({center_y} {app_settings['y_offset']}), Scale: {app_settings['scale']}")

        crop_left = x * scale + app_settings["crop_left"]
        crop_top = y * scale
        crop_right = (screen_width - (x + width)) * scale
        crop_bottom = (screen_height - (y + height)) * scale

        crop_success = await obs_client.set_source_filter_settings(obs_source, "Crop/Pad", {
            "left": crop_left,
            "top": crop_top,
            "right": crop_right,
            "bottom": crop_bottom
        })

        if crop_success:
            print("Crop updated successfully")
        else:
            print("Failed to update crop")

        scaled_width = width * scale
        scaled_height = height * scale

        center_x = (canvas_width - scaled_width) / 2
        center_y = (canvas_height - scaled_height) / 2
        new_x = center_x
        new_y = center_y

        if scaled_width > canvas_width:
            mouse_x_percentage = (mouse_x - x) / width
            if mouse_x_percentage > right_threshold:
                new_x = canvas_width - scaled_width
            elif mouse_x_percentage < left_threshold:
                new_x = 1
            else:
                new_x = center_x  # Center the window if mouse is in the middle

        if scaled_height > canvas_height:
            mouse_y_percentage = (mouse_y - y) / height
            if mouse_y_percentage > bottom_threshold:
                new_y = canvas_height - scaled_height
            elif mouse_y_percentage < top_threshold:
                new_y = 1
            else:
                new_y = center_y

        print(f"App: {app_name}, Target Position: ({new_x}, {center_y}), Scale: {app_settings['scale']}")

        # Animate the transform
        await animate_transform(
            obs_client,
            current_scene,
            source_id,
            current_position["x"] if current_position["x"] != 0 else center_x,
            current_position["y"] if current_position["y"] != 0 else center_y,
            new_x,
            new_y,
            app_settings["scale"] /2
        )

        return crop_success

    except Exception as e:
        print(f"Error in update_obs_crop_and_center: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
