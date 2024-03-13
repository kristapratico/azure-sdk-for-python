# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------


from ._version import VERSION
from ._azure_client import AzureOpenAIClient

__all__ = [
    "AzureOpenAIClient"
]

__version__ = VERSION
