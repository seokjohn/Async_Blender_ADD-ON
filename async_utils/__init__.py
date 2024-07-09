import queue
import asyncio
import threading


global_status_msg = None
global_task_queue = queue.Queue()
global_stop_event = threading.Event()
global_running_event = threading.Event()


def get_global_status_msg():
    return global_status_msg


def update_global_status_msg(msg: str):
    global global_status_msg
    print(msg)
    global_status_msg = msg


def run_async_in_thread(func, *args):
    def thread_async_target():
        asyncio.run(func(*args))

    thread_func = threading.Thread(target=thread_async_target)
    thread_func.start()
