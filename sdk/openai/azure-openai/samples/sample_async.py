
import openai
import pytest
import asyncio
from azure.openai.aio import login
from azure.identity import DefaultAzureCredential


async def login_sample():
    credential = DefaultAzureCredential()
    async with login(endpoint="", credential=credential):
        async def openaicall():
            completion = await openai.Completion.acreate(prompt="hello world", engine="text-davinci-003")
            return completion
        result = await asyncio.gather(
            openaicall(),
            openaicall(),
            openaicall(),
        )
        print(result)
        await credential.close()


asyncio.run(login_sample())