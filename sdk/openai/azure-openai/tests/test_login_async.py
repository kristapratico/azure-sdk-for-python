import openai
import pytest
import asyncio
from azure.openai.aio import login


@pytest.mark.asyncio
async def test_login():
    from azure.identity.aio import DefaultAzureCredential

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