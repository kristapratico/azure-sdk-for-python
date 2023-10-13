# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
import datetime
from typing import List, Any, overload, Optional, Mapping
from .._model_base import rest_field
from .. import models as _models
from ._models import (
    Error,
    InnerError,
    Completions as GeneratedCompletions,
    ChatCompletions as GeneratedChatCompletions,
)


class Completions(GeneratedCompletions):

    id: str = rest_field()
    """A unique identifier associated with this completions response. Required."""
    created: datetime.datetime = rest_field(format="unix-timestamp")
    """The first timestamp associated with generation activity for this completions response,
     represented as seconds since the beginning of the Unix epoch of 00:00 on 1 Jan 1970. Required."""
    prompt_filter_results: Optional[List["_models.PromptFilterResult"]] = rest_field()
    """Content filtering results for zero or more prompts in the request. In a streaming request,
     results for different prompts may arrive at different times or in different orders."""
    choices: List["_models.Choice"] = rest_field()
    """The collection of completions choices associated with this completions response.
     Generally, ``n`` choices are generated per provided prompt with a default value of 1.
     Token limits and other settings may limit the number of choices generated. Required."""
    usage: "_models.CompletionsUsage" = rest_field()
    """Usage information for tokens processed and generated as part of this completions operation.
     Required."""

    @overload
    def __init__(
        self,
        *,
        id: str,  # pylint: disable=redefined-builtin
        created: datetime.datetime,
        choices: List["_models.Choice"],
        usage: "_models.CompletionsUsage",
        prompt_filter_results: Optional[List["_models.PromptFilterResult"]] = None,
    ):
        ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        class_name = self.__class__.__name__
        if len(args) > 1:
            raise TypeError(f"{class_name}.__init__() takes 2 positional arguments but {len(args) + 1} were given")
        if args[0].get("prompt_annotations"):
            args[0]["prompt_filter_results"] = args[0].pop("prompt_annotations")
        super().__init__(*args, **kwargs)


class ChatCompletions(GeneratedChatCompletions):

    id: str = rest_field()
    """A unique identifier associated with this chat completions response. Required."""
    created: datetime.datetime = rest_field(format="unix-timestamp")
    """The first timestamp associated with generation activity for this completions response,
     represented as seconds since the beginning of the Unix epoch of 00:00 on 1 Jan 1970. Required."""
    choices: List["_models.ChatChoice"] = rest_field()
    """The collection of completions choices associated with this completions response.
     Generally, ``n`` choices are generated per provided prompt with a default value of 1.
     Token limits and other settings may limit the number of choices generated. Required."""
    prompt_filter_results: Optional[List["_models.PromptFilterResult"]] = rest_field()
    """Content filtering results for zero or more prompts in the request. In a streaming request,
     results for different prompts may arrive at different times or in different orders."""
    usage: "_models.CompletionsUsage" = rest_field()
    """Usage information for tokens processed and generated as part of this completions operation.
     Required."""

    @overload
    def __init__(
        self,
        *,
        id: str,  # pylint: disable=redefined-builtin
        created: datetime.datetime,
        choices: List["_models.ChatChoice"],
        usage: "_models.CompletionsUsage",
        prompt_filter_results: Optional[List["_models.PromptFilterResult"]] = None,
    ):
        ...

    @overload
    def __init__(self, mapping: Mapping[str, Any]):
        """
        :param mapping: raw JSON to initialize the model.
        :type mapping: Mapping[str, Any]
        """

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
