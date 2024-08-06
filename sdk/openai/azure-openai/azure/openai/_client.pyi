# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from typing import Iterable, overload, Mapping, Union
from typing_extensions import Literal

import httpx
from openai import AzureOpenAI as SyncClient
from openai import Stream
from openai import NotGiven
from openai.types.chat import completion_create_params
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion_stream_options_param import ChatCompletionStreamOptionsParam
from openai.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam
from openai.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from openai.types.chat_model import ChatModel
from openai.resources.chat import Chat as OpenAIChat, Completions as OpenAICompletions

from .types.chat.azure_extensions import AzureChatExtensionConfiguration
from .types.chat.content_filtering import AzureChatCompletionChunk, AzureChatCompletion

class Omit:
    def __bool__(self) -> Literal[False]: ...

Headers = Mapping[str, Union[str, Omit]]
Query = Mapping[str, object]
Body = object


class Completions(OpenAICompletions):
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream: Literal[False] | None | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: AzureChatExtensionConfiguration | None = None) -> AzureChatCompletion: ...
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, stream: Literal[True], frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: AzureChatExtensionConfiguration | None = None) -> Stream[AzureChatCompletionChunk]: ...
    @overload
    def create(self, *, messages: Iterable[ChatCompletionMessageParam], model: str | ChatModel, stream: bool, frequency_penalty: float | None | NotGiven = ..., function_call: completion_create_params.FunctionCall | NotGiven = ..., functions: Iterable[completion_create_params.Function] | NotGiven = ..., logit_bias: dict[str, int] | None | NotGiven = ..., logprobs: bool | None | NotGiven = ..., max_tokens: int | None | NotGiven = ..., n: int | None | NotGiven = ..., parallel_tool_calls: bool | NotGiven = ..., presence_penalty: float | None | NotGiven = ..., response_format: completion_create_params.ResponseFormat | NotGiven = ..., seed: int | None | NotGiven = ..., service_tier: Literal['auto', 'default'] | None | NotGiven = ..., stop: str | None | list[str] | NotGiven = ..., stream_options: ChatCompletionStreamOptionsParam | None | NotGiven = ..., temperature: float | None | NotGiven = ..., tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = ..., tools: Iterable[ChatCompletionToolParam] | NotGiven = ..., top_logprobs: int | None | NotGiven = ..., top_p: float | None | NotGiven = ..., user: str | NotGiven = ..., extra_headers: Headers | None = None, extra_query: Query | None = None, extra_body: Body | None = None, timeout: float | httpx.Timeout | None | NotGiven = ..., data_sources: AzureChatExtensionConfiguration | None = None) -> AzureChatCompletion | Stream[AzureChatCompletionChunk]: ...


class Chat(OpenAIChat):
    completions: Completions


class AzureOpenAI(SyncClient):
    chat: Chat
