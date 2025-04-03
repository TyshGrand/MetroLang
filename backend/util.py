import itertools
import asyncio
import sys
def async_loader(task_name="Processing"):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            spinner = itertools.cycle(['-', '\\', '|', '/'])

            async def loader():
                while True:
                    sys.stdout.write(f"\r{task_name} {next(spinner)}")
                    sys.stdout.flush()
                    await asyncio.sleep(0.1)

            loader_task = asyncio.create_task(loader())
            try:
                return await func(*args, **kwargs)
            finally:
                loader_task.cancel()
                sys.stdout.write("\r" + " " * (len(task_name) + 2) + "\r")
                sys.stdout.flush()

        return wrapper
    return decorator