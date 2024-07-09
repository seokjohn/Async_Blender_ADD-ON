# Aysync Blender ADD-ON
Example code to use async operations (websocket, request) in Blender

### Asynchronous and Threads
When running a task synchronously in Blender, the UI locks up and freezes for the duration of the task. Therefore, long tasks should be made asynchronous. However, running asynchronous tasks in Blender can be quite troublesome. Typically, the Blender API uses a function called a timer to manage this.

**Summary**
1. when using queue in thread, use queue or event queue to proceed
2. when registering timer function, it is registered for each file and needs to be re-registered when loading a new file
3. use of threads is very risky and should be avoided as much as possible by registering timer function

Reference links
- [Error - stackoverflow](https://stackoverflow.com/questions/60831429/blender-api-bpy-and-socket-server)
- [Timer func - blender docs](https://docs.blender.org/api/current/bpy.app.timers.html)
