# obs_client.py

import simpleobsws
import time

class OBSClient:
    def __init__(self, host, port, password):
        self.obs = simpleobsws.WebSocketClient(f"ws://{host}:{port}", password)
        self.current_mode = "scale"
        self.window_position = "center"
        self.current_window = None
        self.last_click_time = 0

    async def connect(self):
        await self.obs.connect()

    async def disconnect(self):
        await self.obs.disconnect()

    async def wait_until_identified(self):
        await self.obs.wait_until_identified()

    async def get_canvas_size(self):
        video_settings_request = simpleobsws.Request('GetVideoSettings')
        video_settings_response = await self.obs.call(video_settings_request)
        if video_settings_response.ok():
            return (
                video_settings_response.responseData['baseWidth'],
                video_settings_response.responseData['baseHeight']
            )
        else:
            print(f"Failed to get canvas size: {video_settings_response.responseData}")
            return None

    async def get_current_scene(self):
        scene_request = simpleobsws.Request('GetCurrentProgramScene')
        scene_response = await self.obs.call(scene_request)
        if scene_response.ok():
            return scene_response.responseData['currentProgramSceneName']
        return None

    async def get_source_id(self, scene_name, source_name):
        items_request = simpleobsws.Request('GetSceneItemList', {"sceneName": scene_name})
        items_response = await self.obs.call(items_request)
        if items_response.ok():
            scene_items = items_response.responseData['sceneItems']
            source_item = next((item for item in scene_items if item['sourceName'] == source_name), None)
            if source_item:
                return source_item['sceneItemId']
        return None

    async def set_source_filter_settings(self, source_name, filter_name, filter_settings):
        request = simpleobsws.Request('SetSourceFilterSettings', {
            "sourceName": source_name,
            "filterName": filter_name,
            "filterSettings": filter_settings
        })
        response = await self.obs.call(request)
        return response.ok()

    async def set_scene_item_transform(self, scene_name, source_id, transform):
        request = simpleobsws.Request('SetSceneItemTransform', {
            "sceneName": scene_name,
            "sceneItemId": source_id,
            "sceneItemTransform": transform
        })
        response = await self.obs.call(request)
        return response.ok()

    async def switch_window(self, new_window):
        if new_window != self.current_window:
            self.current_window = new_window
            self.current_mode = "scale"

    async def handle_mouse_click(self):
        self.last_click_time = time.time()
        if self.current_mode == "scale":
            self.current_mode = "center"
            print(f"❗❗Mode changed to: {self.current_mode}")
