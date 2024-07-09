import bpy
import json
import asyncio
import traceback
import websockets
from bpy.app.handlers import persistent

from . import (
    global_task_queue,
    global_stop_event,
    global_running_event,
    update_global_status_msg
)


async def socket_connection_func(ws_url: str):
    try:
        async with websockets.connect(ws_url) as ws:
            update_global_status_msg("Connected to socket server")
            while not global_stop_event.is_set():
                if 1 < ws.state:
                    print(f"websocket state: {ws.state}")
                    break

                try:
                    message = await asyncio.wait_for(ws.recv(), 3)
                except Exception:
                    message = None

                if message:
                    message_dict = json.loads(message)
                    update_global_status_msg("Sync in progress...")
                    global_task_queue.put(message_dict)
                    if not register_timer_func in bpy.app.handlers.load_post:
                        update_global_status_msg("Reloading Blender App or File")

    except Exception:
        traceback.print_exc()
    finally:
        global_stop_event.clear()
        global_running_event.clear()
        update_global_status_msg("Disconnected to socket server")


def download_or_merge_file_timer_func():
    try:
        while not global_task_queue.empty():
            data = global_task_queue.get()
            print(data)
            #Add download code or brander control code

    except Exception:
        traceback.print_exc()
    finally:
        return 0.3



@persistent
def register_timer_func(*args):
    print("load blender file")
    if not bpy.app.timers.is_registered(download_or_merge_file_timer_func):
        print("register timer func")
        bpy.app.timers.register(download_or_merge_file_timer_func)


@persistent
def unregister_timer_func():
    if bpy.app.timers.is_registered(download_or_merge_file_timer_func):
        bpy.app.timers.unregister(download_or_merge_file_timer_func)
