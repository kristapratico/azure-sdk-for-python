# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
import json
import datetime
from typing import Any, List, Union, TYPE_CHECKING, overload, Optional
from azure.core.tracing.decorator import distributed_trace
from azure.core.paging import ItemPaged
from azure.core.credentials import AzureKeyCredential
from ._client import DocumentTranslationClient as GeneratedDocumentTranslationClient
from ._user_agent import USER_AGENT
from ._polling import TranslationPolling, DocumentTranslationLROPollingMethod, DocumentTranslationLROPoller
from ._helpers import (
    get_http_logging_policy,
    convert_datetime,
    convert_order_by,
    get_authentication_policy,
    get_translation_input,
    POLLING_INTERVAL,
)
if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential



def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """


class DocumentTranslationClient(GeneratedDocumentTranslationClient):
    def __init__(
        self,
        endpoint: str,
        credential: Union[AzureKeyCredential, "TokenCredential"],
        **kwargs: Any
    ) -> None:
        """DocumentTranslationClient is your interface to the Document Translation service.
        Use the client to translate whole documents while preserving source document
        structure and text formatting.

        :param str endpoint: Supported Document Translation endpoint (protocol and hostname, for example:
            https://<resource-name>.cognitiveservices.azure.com/).
        :param credential: Credentials needed for the client to connect to Azure.
            This is an instance of AzureKeyCredential if using an API key or a token
            credential from :mod:`azure.identity`.
        :type credential: :class:`~azure.core.credentials.AzureKeyCredential` or
            :class:`~azure.core.credentials.TokenCredential`
        :keyword api_version:
            The API version of the service to use for requests. It defaults to the latest service version.
            Setting to an older version may result in reduced feature compatibility.
        :paramtype api_version: str or ~azure.ai.translation.document.DocumentTranslationApiVersion

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_authentication.py
                :start-after: [START create_dt_client_with_key]
                :end-before: [END create_dt_client_with_key]
                :language: python
                :dedent: 4
                :caption: Creating the DocumentTranslationClient with an endpoint and API key.

            .. literalinclude:: ../samples/sample_authentication.py
                :start-after: [START create_dt_client_with_aad]
                :end-before: [END create_dt_client_with_aad]
                :language: python
                :dedent: 4
                :caption: Creating the DocumentTranslationClient with a token credential.
        """
        try:
            self._endpoint = endpoint.rstrip("/")
        except AttributeError:
            raise ValueError("Parameter 'endpoint' must be a string.")
        self._credential = credential
        self._api_version = kwargs.pop("api_version", None)

        authentication_policy = get_authentication_policy(credential)
        polling_interval = kwargs.pop("polling_interval", POLLING_INTERVAL)

        super().__init__(
            endpoint=self._endpoint,
            credential=credential,  # type: ignore
            api_version=self._api_version,
            sdk_moniker=USER_AGENT,
            authentication_policy=kwargs.pop("authentication_policy", authentication_policy),
            http_logging_policy=kwargs.pop("http_logging_policy", get_http_logging_policy()),
            polling_interval=polling_interval,
            **kwargs
        )




__all__: List[str] = ["DocumentTranslationClient"]  # Add all objects you want publicly available to users at this package level