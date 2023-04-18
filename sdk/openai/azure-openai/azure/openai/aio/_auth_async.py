# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import typing
import time
import logging
import asyncio
import openai

log = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from azure.core.credentials_async import AsyncTokenCredential

try:
    import aiohttp
except ModuleNotFoundError:
    print(
        "You have to install the `aiohttp` library in order to use azure.openai.aio"
    )
    exit(-1)


class AsyncTokenCredentialAuth(aiohttp.ClientRequest):

    async def _refresh_token(self):
        if self.props.get("cached_token") is None or self.props.get("cached_token").expires_on - time.time() < 300:
            async with self.props.get("lock"):
                if self.props.get("cached_token") is None or self.props.get("cached_token").expires_on - time.time() < 300:
                    self.props["cached_token"] = await self.props["credential"].get_token(*self.props.get("scopes"))
        self.headers["Authorization"] = "Bearer " + self.props["cached_token"].token

    async def send(self, conn: "aiohttp.Connection") -> "aiohttp.ClientResponse":
        await self._refresh_token()
        return await super().send(conn)


def login(
    endpoint: str, credential: "AsyncTokenCredential", *, scopes: typing.Union[str, typing.List[str]], api_version: typing.Optional[str] = None
) -> None:
    if openai.api_version and api_version:
        log.info(f'Overriding openai.api_version "{openai.api_version}" with api_version "{api_version}" passed to azure.openai.aio.login') 
    openai.api_version = api_version or openai.api_version or '2022-12-01'
    
    if openai.api_base and endpoint != openai.api_base:
        log.info(f'Overriding openai.api_base "{openai.api_base}" with endpoint "{endpoint}" passed to azure.openai.aio.login')
    openai.api_base = endpoint
    openai.api_key = "AZUREAD_FAKE_API_KEY"
    openai.api_type = "azuread"

    scopes = [scopes] if isinstance(scopes, str) else scopes
    if scopes is None:
        scopes = ["https://cognitiveservices.azure.com/.default"]

    request_class = AsyncTokenCredentialAuth
    request_class.props = {"credential": credential, "scopes": scopes, "cached_token": None, "lock": asyncio.Lock()}
    session = aiohttp.ClientSession(request_class=AsyncTokenCredentialAuth)
    openai.aiosession.set(session)
    return session
