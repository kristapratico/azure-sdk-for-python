# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
from typing import Optional, Union, List
import time
import logging
import requests
import openai
from azure.core.credentials import AzureKeyCredential, TokenCredential


log = logging.getLogger(__name__)


class CredentialRefresh:

    def __init__(self, credential: Union[TokenCredential, AzureKeyCredential], *scopes: str) -> None:
        self.credential = credential
        self.scopes = scopes
        self.cached_token: Optional[str] = None

    def __call__(self, req):
        if isinstance(self.credential, AzureKeyCredential):
            req.headers["api-key"] = self.credential.key
            return req
        if not self.cached_token or self.cached_token.expires_on - time.time() < 300:
            self.cached_token = self.credential.get_token(*self.scopes)
        req.headers["Authorization"] = f"Bearer {self.cached_token.token}"
        return req


# let the user to pass session?
def login(
    *,
    api_key: Optional[Union[str, AzureKeyCredential, TokenCredential]] = None,
    api_key_path: Optional[str] = None,
    api_base: Optional[str] = None,
    api_type: Optional[str] = None,
    api_version: Optional[str] = None,
    organization: Optional[str] = None,
    scopes: Optional[Union[str, List[str]]] = None,
) -> None:

    session = requests.Session()  # match openai config?

    if api_base:
        openai.api_base = api_base

    if api_key_path:
        openai.api_key_path = api_key_path

    if organization:
        openai.organization = organization

    if api_type:
        openai.api_type = api_type

    if api_version:
        openai.api_version = api_version

    if openai.api_version is None:
        openai.api_version = os.getenv("OPENAI_API_VERSION", "2022-12-01")  # API version is not configured by env var in openai yet

    if hasattr(api_key, "get_token"):
        openai.api_type = "azuread"
        openai.api_key = "API_KEY"
        scopes = [scopes] if isinstance(scopes, str) else scopes
        if scopes is None:
            scopes = ["https://cognitiveservices.azure.com/.default"]
        session.auth = CredentialRefresh(api_key, *scopes)

    elif isinstance(api_key, AzureKeyCredential):
        openai.api_type = "azure"
        openai.api_key = api_key.key
        session.auth = CredentialRefresh(api_key)

    elif api_key:
        # can we assume that api_key will have prefix "sk" if it's OAI and set api_type?
        # should we use api_base to inform the api_type and api_version?
        # do we want to control the session if it's OAI?
        openai.api_key = api_key

    openai.requestssession = session
    return session
