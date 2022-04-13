# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List

import json
import datetime
from typing import Any, List, Union, TYPE_CHECKING, overload, Optional
from azure.core.tracing.decorator import distributed_trace
from azure.core.paging import ItemPaged
from azure.core.credentials import AzureKeyCredential
from .._helpers import (
    get_http_logging_policy,
    convert_datetime,
    convert_order_by,
    get_authentication_policy,
    get_translation_input,
    POLLING_INTERVAL,
)

from ._operations import DocumentTranslationOperations as GeneratedDocumentTranslationOperations

def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """


class DocTranslationOperations(GeneratedDocumentTranslationOperations):
    ...



__all__: List[str] = []  # Add all objects you want publicly available to users at this package level
