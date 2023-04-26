# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import typing
import time
import logging
import openai
log = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    from azure.core.credentials import TokenCredential

try:
    import requests
except ModuleNotFoundError:
    print(
        "You have to install the `requests` library in order to use azure.openai"
    )
    exit(-1)


class TokenCredentialAuth:

    def __init__(self, credential: "TokenCredential", *scopes: str) -> None:
        self.credential = credential
        self.scopes = scopes
        self.cached_token: typing.Optional[str] = None

    def __call__(self, req):
        if not self.cached_token or self.cached_token.expires_on - time.time() < 300:
            self.cached_token = self.credential.get_token(*self.scopes)
        req.headers["Authorization"] = f"Bearer {self.cached_token.token}"
        return req


def login(
    endpoint: str,
    credential: "TokenCredential",
    *,
    scopes: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    api_version: typing.Optional[str] = None
) -> None:
    if openai.api_version and api_version:
        log.info(f'Overriding openai.api_version "{openai.api_version}" with api_version "{api_version}" passed to azure.openai.login') 
    openai.api_version = api_version or openai.api_version or '2022-12-01'

    if openai.api_base and endpoint != openai.api_base:
        log.info(f'Overriding openai.api_base "{openai.api_base}" with endpoint "{endpoint}" passed to azure.openai.login')
    openai.api_base = endpoint
    openai.api_key = "AZUREAD_FAKE_API_KEY"
    openai.api_type = "azuread"

    scopes = [scopes] if isinstance(scopes, str) else scopes
    if scopes is None:
        scopes = ["https://cognitiveservices.azure.com/.default"]

    # should this use a session factory instead? i.e a session per thread
    session = requests.Session()
    session.auth = TokenCredentialAuth(credential, *scopes)
    openai.requestssession = session
    return session
