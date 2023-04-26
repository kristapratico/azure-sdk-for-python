import openai
import logging
import typing
import requests
import aiohttp
import asyncio
import time
if typing.TYPE_CHECKING:
    from azure.core.credentials import TokenCredential
    from azure.core.credentials_async import AsyncTokenCredential
log = logging.getLogger(__name__)

import openai
import pytest
import asyncio
from azure.openai import login



def test_login():
    from azure.identity import DefaultAzureCredential

    credential = DefaultAzureCredential()
    with login(endpoint="", credential=credential):
        completion = openai.Completion.create(prompt="hello", engine="text-davinci-003")
        assert completion
