bl_info = {
    "name": "Async Task Add ON",
    "description": "An example add-on for async tasks in Blender",
    "author": "Seok Yo han",
    "version": (0, 0, 1),
    "doc_url": "https://github.com/benrugg/AI-Render#readme",
    "tracker_url": "https://github.com/seokjohn",
    "category": "3D View",
}


import os
import sys
import subprocess
import importlib.util


with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as f:
    module_names = f.read().splitlines()
    for module_name in module_names:
        real_module_name = module_name.split("=", 1)[0]
        if not importlib.util.find_spec(real_module_name):
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])


if "bpy" in locals():
    import imp
    imp.reload(penals)
    imp.reload(async_utils)

else:
    from . import (
        penals
    )
    from . import (
        async_utils
    )


def register():
    penals.register()


def unregister():
    penals.unregister()


if __name__ == "__main__":
    register()
