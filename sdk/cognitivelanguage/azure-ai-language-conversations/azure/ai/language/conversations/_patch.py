# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, overload, Union, IO, Any
from azure.core.tracing.decorator import distributed_trace
from ._client import ConversationAnalysisClient as GeneratedConversationAnalysisClient
from ._operations._operations import JSON


class ConversationAnalysisClient(GeneratedConversationAnalysisClient):
    @overload
    def analyze_conversation(self, task: JSON, *, content_type: str = "application/json", **kwargs: Any) -> JSON:
        ...

    @overload
    def analyze_conversation(self, task: IO, *, content_type: str = "application/json", **kwargs: Any) -> JSON:
        ...

    @distributed_trace
    def analyze_conversation(self, task: Union[JSON, IO], **kwargs: Any) -> JSON:
        return super().analyze_conversation(task, **kwargs)


__all__: List[str] = [
    "ConversationAnalysisClient",
]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
