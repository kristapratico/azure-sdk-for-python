# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from __future__ import annotations
import functools
from typing import Iterable, overload, Mapping, Union, TypeVar, Callable

from typing_extensions import Literal, ParamSpec
import httpx
from openai import Stream, NotGiven, AzureOpenAI as SyncClient
from openai.types.chat import completion_create_params, ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat_model import ChatModel
from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_response_format_option_param import AssistantResponseFormatOptionParam
from openai.types.beta import assistant_create_params
from openai.resources.beta import Beta as OpenAIBeta
from openai.resources.beta.assistants import Assistants as OpenAIAssistants
from openai.resources.chat import Chat as OpenAIChat, Completions as OpenAICompletions

from azure.openai.types.chat.azure_extras import AzureChatExtras
from azure.openai.types.beta.assistants import AzureAssistantToolParam
from azure.openai.types.chat import AzureChatCompletion
from azure.openai.types.chat import AzureChatCompletionChunk
from azure.openai.types.beta.assistants import AzureAssistant

_P = ParamSpec("_P")
_R = TypeVar("_R")

class Omit:
    def __bool__(self) -> Literal[False]: ...

Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object

class Completions(OpenAICompletions):
    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: str | ChatModel,
        frequency_penalty: float | None | NotGiven = ...,
        function_call: completion_create_params.FunctionCall | NotGiven = ...,
        functions: Iterable[completion_create_params.Function] | NotGiven = ...,
        logit_bias: dict[str, int] | None | NotGiven = ...,
        logprobs: bool | None | NotGiven = ...,
        max_tokens: int | None | NotGiven = ...,
        n: int | None | NotGiven = ...,
        parallel_tool_calls: bool | NotGiven = ...,
        presence_penalty: float | None | NotGiven = ...,
        response_format: completion_create_params.ResponseFormat | NotGiven = ...,
        seed: int | None | NotGiven = ...,
        service_tier: Literal["auto", "default"] | None | NotGiven = ...,
        stop: str | None | list[str] | NotGiven = ...,
        stream: Literal[False] | None | NotGiven = ...,
        stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ...,
        temperature: float | None | NotGiven = ...,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ...,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = ...,
        top_logprobs: int | None | NotGiven = ...,
        top_p: float | None | NotGiven = ...,
        user: str | NotGiven = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: AzureChatExtras | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = ...,
    ) -> ChatCompletion: ...
    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: str | ChatModel,
        stream: Literal[True],
        frequency_penalty: float | None | NotGiven = ...,
        function_call: completion_create_params.FunctionCall | NotGiven = ...,
        functions: Iterable[completion_create_params.Function] | NotGiven = ...,
        logit_bias: dict[str, int] | None | NotGiven = ...,
        logprobs: bool | None | NotGiven = ...,
        max_tokens: int | None | NotGiven = ...,
        n: int | None | NotGiven = ...,
        parallel_tool_calls: bool | NotGiven = ...,
        presence_penalty: float | None | NotGiven = ...,
        response_format: completion_create_params.ResponseFormat | NotGiven = ...,
        seed: int | None | NotGiven = ...,
        service_tier: Literal["auto", "default"] | None | NotGiven = ...,
        stop: str | None | list[str] | NotGiven = ...,
        stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ...,
        temperature: float | None | NotGiven = ...,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ...,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = ...,
        top_logprobs: int | None | NotGiven = ...,
        top_p: float | None | NotGiven = ...,
        user: str | NotGiven = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: AzureChatExtras | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = ...,
    ) -> Stream[ChatCompletionChunk]: ...
    @overload
    def create(
        self,
        *,
        messages: Iterable[ChatCompletionMessageParam],
        model: str | ChatModel,
        stream: bool,
        frequency_penalty: float | None | NotGiven = ...,
        function_call: completion_create_params.FunctionCall | NotGiven = ...,
        functions: Iterable[completion_create_params.Function] | NotGiven = ...,
        logit_bias: dict[str, int] | None | NotGiven = ...,
        logprobs: bool | None | NotGiven = ...,
        max_tokens: int | None | NotGiven = ...,
        n: int | None | NotGiven = ...,
        parallel_tool_calls: bool | NotGiven = ...,
        presence_penalty: float | None | NotGiven = ...,
        response_format: completion_create_params.ResponseFormat | NotGiven = ...,
        seed: int | None | NotGiven = ...,
        service_tier: Literal["auto", "default"] | None | NotGiven = ...,
        stop: str | None | list[str] | NotGiven = ...,
        stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ...,
        temperature: float | None | NotGiven = ...,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ...,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = ...,
        top_logprobs: int | None | NotGiven = ...,
        top_p: float | None | NotGiven = ...,
        user: str | NotGiven = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: AzureChatExtras | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = ...,
    ) -> ChatCompletion | Stream[ChatCompletionChunk]: ...

class Chat(OpenAIChat):
    completions: Completions

class Assistants(OpenAIAssistants):
    def create(
        self,
        *,
        model: (
            str
            | Literal[
                "gpt-4o",
                "gpt-4o-2024-05-13",
                "gpt-4o-mini",
                "gpt-4o-mini-2024-07-18",
                "gpt-4-turbo",
                "gpt-4-turbo-2024-04-09",
                "gpt-4-0125-preview",
                "gpt-4-turbo-preview",
                "gpt-4-1106-preview",
                "gpt-4-vision-preview",
                "gpt-4",
                "gpt-4-0314",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0314",
                "gpt-4-32k-0613",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-1106",
                "gpt-3.5-turbo-0125",
                "gpt-3.5-turbo-16k-0613",
            ]
        ),
        description: str | None | NotGiven = ...,
        instructions: str | None | NotGiven = ...,
        metadata: object | None | NotGiven = ...,
        name: str | None | NotGiven = ...,
        response_format: AssistantResponseFormatOptionParam | None | NotGiven = ...,
        temperature: float | None | NotGiven = ...,
        tool_resources: assistant_create_params.ToolResources | None | NotGiven = ...,
        tools: Iterable[AzureAssistantToolParam] | NotGiven = ...,
        top_p: float | None | NotGiven = ...,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = ...,
    ) -> Assistant: ...

class Beta(OpenAIBeta):
    assistants: Assistants

class AzureOpenAI(SyncClient):
    chat: Chat
    beta: Beta

@overload
def parse_azure(model: Assistant) -> AzureAssistant: ...
@overload
def parse_azure(model: ChatCompletionChunk) -> AzureChatCompletionChunk: ...
@overload
def parse_azure(model: ChatCompletion) -> AzureChatCompletion: ...

def parse_azure_wrapper(func: Callable[_P, _R]) -> Callable[_P, _R]:
    @functools.wraps(func)
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _R: ...
