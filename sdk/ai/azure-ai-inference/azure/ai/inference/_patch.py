# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
# pylint: disable=too-many-lines)
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize

Why do we patch auto-generated code?
1. Add support for input argument `model_extras` (all clients)
2. Add support for function load_client
3. Add support for setting sticky chat completions/embeddings input arguments in the client constructor
4. Add support for get_model_info, while caching the result (all clients)
5. Add support for chat completion streaming (ChatCompletionsClient client only)
6. Add support for friendly print of result objects (__str__ method) (all clients)
7. Add support for load() method in ImageUrl class (see /models/_patch.py).

"""

import logging
from typing import Any, Union, List, TYPE_CHECKING

from azure.core.credentials import AzureKeyCredential

from . import models as _models
from ._client import ChatCompletionsClient
from ._client import EmbeddingsClient
from ._client import ImageEmbeddingsClient

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from azure.core.credentials import TokenCredential


_LOGGER = logging.getLogger(__name__)


def load_client(
    endpoint: str, credential: Union[AzureKeyCredential, "TokenCredential"], **kwargs: Any
) -> Union["ChatCompletionsClient", "EmbeddingsClient", "ImageEmbeddingsClient"]:
    """
    Load a client from a given endpoint URL. The method makes a REST API call to the `/info` route
    on the given endpoint, to determine the model type and therefore which client to instantiate.
    This method will only work when using Serverless API or Managed Compute endpoint.
    It will not work for GitHub Models endpoint or Azure OpenAI endpoint.

    :param endpoint: Service host. Required.
    :type endpoint: str
    :param credential: Credential used to authenticate requests to the service. Is either a
     AzureKeyCredential type or a TokenCredential type. Required.
    :type credential: ~azure.core.credentials.AzureKeyCredential or
     ~azure.core.credentials.TokenCredential
    :keyword api_version: The API version to use for this operation. Default value is
     "2024-05-01-preview". Note that overriding this default value may result in unsupported
     behavior.
    :paramtype api_version: str
    :return: The appropriate synchronous client associated with the given endpoint
    :rtype: ~azure.ai.inference.ChatCompletionsClient or ~azure.ai.inference.EmbeddingsClient
     or ~azure.ai.inference.ImageEmbeddingsClient
    :raises ~azure.core.exceptions.HttpResponseError:
    """

    with ChatCompletionsClient(
        endpoint, credential, **kwargs
    ) as client:  # Pick any of the clients, it does not matter.
        model_info = client.get_model_info()  # type: ignore

    _LOGGER.info("model_info=%s", model_info)
    if not model_info.model_type:
        raise ValueError(
            "The AI model information is missing a value for `model type`. Cannot create an appropriate client."
        )

    # TODO: Remove "completions" and "embedding" once Mistral Large and Cohere fixes their model type
    if model_info.model_type in (_models.ModelType.CHAT, "completion"):
        chat_completion_client = ChatCompletionsClient(endpoint, credential, **kwargs)
        chat_completion_client._model_info = (  # pylint: disable=protected-access,attribute-defined-outside-init
            model_info
        )
        return chat_completion_client

    if model_info.model_type in (_models.ModelType.EMBEDDINGS, "embedding"):
        embedding_client = EmbeddingsClient(endpoint, credential, **kwargs)
        embedding_client._model_info = model_info  # pylint: disable=protected-access,attribute-defined-outside-init
        return embedding_client

    if model_info.model_type == _models.ModelType.IMAGE_EMBEDDINGS:
        image_embedding_client = ImageEmbeddingsClient(endpoint, credential, **kwargs)
        image_embedding_client._model_info = (  # pylint: disable=protected-access,attribute-defined-outside-init
            model_info
        )
        return image_embedding_client

    raise ValueError(f"No client available to support AI model type `{model_info.model_type}`")


__all__: List[str] = [
    "load_client",
]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
