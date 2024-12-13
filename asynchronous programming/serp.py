import time
import asyncio

async def tokenizer(a):
	await asyncio.create_task()

async def findOnSerp(a, b,c, d):
	await asyncio.sleep(2)

async def openai():
	await asyncio.sleep(2)

async def run(x):
    paragraph = "ANSWER: "
	paragraph = findOnSerp(12,34,45,34)
    # print(paragraph)
	# input_tokens = tokenizer(paragraph)
	# response = openai()

if __name__ == "__main__":
    asyncio.run(run(1))