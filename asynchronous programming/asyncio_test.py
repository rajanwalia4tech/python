import asyncio
import time
print(asyncio)
async def wait(n):
    await asyncio.sleep(n)
    print(f"Waited {n} seconds")
    return f"Done {n}"

async def main():
    # asyncio.run(wait(5))
    print(time.strftime("%X"))
    # task1 = await asyncio.create_task(wait(2)) # create_task will create a coroutine
    # task2 = await asyncio.create_task(wait(3)) # create_task will create a coroutine
    # print(task1, task2)
    task1 = asyncio.create_task(wait(2))
    task2 = asyncio.create_task(wait(1))
    print(task1, task2)
    print(await task1)
    print(await task2)

    print(time.strftime("%X"))

if(__name__ == "__main__"):
    asyncio.run(main())
