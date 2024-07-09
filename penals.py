import bpy
from .async_utils import (
    global_stop_event,
    global_running_event,
    get_global_status_msg,
    run_async_in_thread
)
from .async_utils.websocket import (
    socket_connection_func,
    register_timer_func,
    unregister_timer_func
)
from .async_utils.request import download_file


class AsyncProperties(bpy.types.PropertyGroup):
    websocket_url : bpy.props.StringProperty(
        default="",
    ) # type: ignore
    
    download_url: bpy.props.StringProperty(
        default="",
    ) # type: ignore
    
    save_file_path: bpy.props.StringProperty(
        default="",
    ) # type: ignore


class VIEW3D_PT_AsyncTask(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_async_task"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = "Async Task Add-ON"
    bl_category = "Async Task"

    def draw(self, context):
        layout = self.layout
        props = context.scene.async_task

        row = layout.row()
        row.label(text=f"Current Status: {get_global_status_msg()}")
        row.separator()

        layout.label(text="Async Websocket", icon='INFO')
        row = layout.row()
        row.prop(props, "websocket_url", text="Websocket URL")
        layout.operator("async_task.websocket_operator", text="Connect or Disconnect")
        layout.separator()
    
        layout.label(text="Async Request", icon='INFO')
        row = layout.row()
        row.prop(props, "download_url", text="Download URL")
        row = layout.row()
        row.prop(props, "save_file_path", text="Save Path")
        layout.operator("async_task.request_operator", text="Send Request")
        layout.separator()


class AsyncTaskWebsocketOperator(bpy.types.Operator):
    bl_idname = "async_task.websocket_operator"
    bl_label = "WebSocket Connect/Disconnect"

    def execute(self, context):
        scene = context.scene
        if not global_running_event.is_set():
            global_running_event.set()
            run_async_in_thread(socket_connection_func, scene.async_task.websocket_url)
        else:
            global_stop_event.set()
        return {'FINISHED'}


class AsyncTaskRequestOperator(bpy.types.Operator):
    bl_idname = "async_task.request_operator"
    bl_label = "Send Download Request"

    def execute(self, context):
        scene = context.scene
        run_async_in_thread(download_file, scene.async_task.download_url, scene.async_task.save_file_path)
        return {'FINISHED'}


classes = [
    AsyncProperties,
    VIEW3D_PT_AsyncTask,
    AsyncTaskWebsocketOperator,
    AsyncTaskRequestOperator
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.async_task = bpy.props.PointerProperty(type=AsyncProperties)

    global_stop_event.clear()
    global_running_event.clear()

    # Register timer func for each new file call
    bpy.app.handlers.load_post.append(register_timer_func)


def unregister():
    global_stop_event.set()

    # Remove an existing registered timer func
    if unregister_timer_func in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(unregister_timer_func)

    del bpy.types.Scene.async_task

    for cls in classes:
        bpy.utils.unregister_class(cls)
