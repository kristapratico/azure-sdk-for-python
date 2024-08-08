# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from __future__ import annotations
from typing import Iterable, overload, Mapping, Union, List

from typing_extensions import Literal, TypedDict, TypeAlias
import httpx

from openai import AzureOpenAI as SyncClient
from openai import Stream, NotGiven
from openai.types.chat import completion_create_params
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat_model import ChatModel
from openai.resources.chat import Chat as OpenAIChat, Completions as OpenAICompletions
from openai.resources.beta import Beta as OpenAIBeta
from openai.resources.beta.assistants import Assistants as OpenAIAssistants
from openai.types.beta.assistant import Assistant
from openai.types.beta.assistant_response_format_option_param import AssistantResponseFormatOptionParam
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai.types.beta import assistant_create_params

from .types.chat.on_your_data import AzureChatExtensionConfiguration
from .types.chat._content_filtering import AzureChatCompletionChunk, AzureChatCompletion


class Omit:
    def __bool__(self) -> Literal[False]: ...

Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object


class Completions(OpenAICompletions):
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream: Literal[False] | None | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: List[AzureChatExtensionConfiguration] | None = None) -> AzureChatCompletion: ...
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, stream: Literal[True], frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: List[AzureChatExtensionConfiguration] | None = None) -> Stream[AzureChatCompletionChunk]: ...
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, stream: bool, frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: List[AzureChatExtensionConfiguration] | None = None) -> AzureChatCompletion | Stream[AzureChatCompletionChunk]: ...


class Chat(OpenAIChat):
    completions: Completions


class BrowserToolParam(TypedDict, total=False):
    type: Literal["browser"]
    browser: object


AzureAssistantToolParam: TypeAlias = Union[BrowserToolParam, AssistantToolParam]


class Assistants(OpenAIAssistants):
    def create(self, *, model: str | Literal['gpt-4o', 'gpt-4o-2024-05-13', 'gpt-4o-mini', 'gpt-4o-mini-2024-07-18', 'gpt-4-turbo', 'gpt-4-turbo-2024-04-09', 'gpt-4-0125-preview', 'gpt-4-turbo-preview', 'gpt-4-1106-preview', 'gpt-4-vision-preview', 'gpt-4', 'gpt-4-0314', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0314', 'gpt-4-32k-0613', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-1106', 'gpt-3.5-turbo-0125', 'gpt-3.5-turbo-16k-0613'], description: str | None | NotGiven = ..., instructions: str | None | NotGiven = ..., metadata: object | None | NotGiven = ..., name: str | None | NotGiven = ..., response_format: AssistantResponseFormatOptionParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_resources: assistant_create_params.ToolResources | None | NotGiven = ..., tools: Iterable[AzureAssistantToolParam] | NotGiven = ..., top_p: float | None | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ...) -> Assistant: ...


class Beta(OpenAIBeta):
    assistants: Assistants


class AzureOpenAI(SyncClient):
    chat: Chat
    beta: Beta