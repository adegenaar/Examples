import asyncio
from asyncio import Queue
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def concurrent(name: str) -> str:
    print(f"concurrent {name}: started at {time.strftime('%X')}")

    await asyncio.gather(
        say_after(2, f"concurrent {name}: hello"), say_after(2, "concurrent: world")
    )

    print(f"concurrent {name}: finished at {time.strftime('%X')}")
    return name


async def sequential(name: str) -> str:
    print(f"sequential {name}:started at {time.strftime('%X')}")

    await say_after(2, f"sequential {name}: hello")
    await say_after(2, f"sequential {name}: world")

    print(f"sequential {name}: finished at {time.strftime('%X')}")
    return name


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        task = await queue.get()
        results = await task
        task.result = results

        # Notify the queue that the "work item" has been processed.
        queue.task_done()
        print(f"{name} finished")


async def main():
    # Create a queue that we will use to store our "workload".
    queue = Queue()
    await queue.put(sequential("one"))
    await queue.put(concurrent("two"))
    await queue.put(sequential("three"))

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(2):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    await queue.join()

    # Shutdown our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
