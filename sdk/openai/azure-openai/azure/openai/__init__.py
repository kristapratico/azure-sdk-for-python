# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from typing import overload, TypeVar, Callable
import functools

from typing_extensions import ParamSpec
from openai import AzureOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.beta.assistant import Assistant
from azure.openai.types.chat import AzureChatCompletion, AzureChatCompletionChunk
from azure.openai.types.beta.assistants import AzureAssistant
from ._version import VERSION

__version__ = VERSION

_P = ParamSpec("_P")
_R = TypeVar("_R")


@overload
def parse_azure(model: Assistant) -> AzureAssistant: ...
@overload
def parse_azure(model: ChatCompletionChunk) -> AzureChatCompletionChunk: ...
@overload
def parse_azure(model: ChatCompletion) -> AzureChatCompletion: ...
def parse_azure(model):
    # TODO instead of isinstance, may be able to use object property literal value
    if isinstance(model, Assistant):
        return AzureAssistant.construct(_fields_set=None, **model.to_dict(warnings=False))
    if isinstance(model, ChatCompletionChunk):
        return AzureChatCompletionChunk.construct(_fields_set=None, **model.to_dict(warnings=False))
    if isinstance(model, ChatCompletion):
        return AzureChatCompletion.construct(_fields_set=None, **model.to_dict(warnings=False))
    return model


def parse_azure_wrapper(func: Callable[_P, _R]) -> Callable[_P, _R]:
    @functools.wraps(func)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        azure_type = parse_azure(args[1])
        new_args = args[0], azure_type
        return func(*new_args, **kwargs)

    return inner


__all__ = ["AzureOpenAI", "parse_azure", "parse_azure_wrapper"]
