import aiohttp
import asyncio
import time

async def fetchFromGoogle():
    url = "https://www.google.com"
    session = aiohttp.ClientSession()
    response = await session.get(url)
    print(f"Status: {response.status} {await response.content.read(50)}")
    await session.close()

async def main():
    print(time.strftime("%X"))
    await asyncio.gather(fetchFromGoogle(), fetchFromGoogle(), fetchFromGoogle()) # gather will create a coroutine
    print(time.strftime("%X"))

if(__name__ == "__main__"):
    asyncio.run(main())