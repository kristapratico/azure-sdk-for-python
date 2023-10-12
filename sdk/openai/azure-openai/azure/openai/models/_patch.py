# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
import datetime
from typing import List, Any, overload, Optional, Mapping, List
from ._models import (
    Error,
    InnerError,
    Completions as GeneratedCompletions,
    ChatCompletions as GeneratedChatCompletions,
    Choice,
    ChatChoice,
    CompletionsUsage,
    PromptFilterResult
)


class Completions(GeneratedCompletions):
    @overload
    def __init__(
        self,
        *,
        id: str,  # pylint: disable=redefined-builtin
        created: datetime.datetime,
        choices: List[Choice],
        usage: CompletionsUsage,
        prompt_filter_results: Optional[List[PromptFilterResult]] = None,
    ):
        ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        class_name = self.__class__.__name__
        if len(args) > 1:
            raise TypeError(f"{class_name}.__init__() takes 2 positional arguments but {len(args) + 1} were given")
        if args[0].get("prompt_annotations"):
            args[0]["prompt_filter_results"] = args[0].pop("prompt_annotations")
        super().__init__(*args, **kwargs)


class ChatCompletions(GeneratedChatCompletions):
    @overload
    def __init__(
        self,
        *,
        id: str,  # pylint: disable=redefined-builtin
        created: datetime.datetime,
        choices: List[ChatChoice],
        usage: CompletionsUsage,
        prompt_filter_results: Optional[List[PromptFilterResult]] = None,
    ):
        ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        class_name = self.__class__.__name__
        if len(args) > 1:
            raise TypeError(f"{class_name}.__init__() takes 2 positional arguments but {len(args) + 1} were given")
        if args[0].get("prompt_annotations"):
            args[0]["prompt_filter_results"] = args[0].pop("prompt_annotations")
        super().__init__(*args, **kwargs)


__all__: List[str] = [
    "Error",
    "InnerError",
    "Completions",
    "ChatCompletions",
]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
