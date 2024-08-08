# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from typing import List, Optional
from typing_extensions import Literal
from openai import BaseModel

from openai.types.chat import ChatCompletion, ChatCompletionChunk, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice as ChatChoice
from openai.types.chat.chat_completion_chunk import ChoiceDelta, Choice as ChatChoiceDelta
from openai.types.completion import Completion
from openai.types.completion_choice import CompletionChoice

AzureChatCompletionRole = Literal["system", "user", "assistant", "function", "tool"]

class ContentFilterResult(BaseModel):
    severity: Literal["safe", "low", "medium", "high"]
    filtered: bool


class Error(BaseModel):
    code: str
    message: str


class ContentFilterResults(BaseModel):
    hate: Optional[ContentFilterResult]
    self_harm: Optional[ContentFilterResult]
    violence: Optional[ContentFilterResult]
    sexual: Optional[ContentFilterResult]
    error: Optional[Error]


class PromptFilterResult(BaseModel):
    prompt_index: int
    content_filter_results: Optional[ContentFilterResults]


class AzureChatExtensionsMessageContext(BaseModel):
    messages: Optional[List[ChatCompletionMessage]]


class AzureChatCompletionMessage(ChatCompletionMessage):
    context: Optional[AzureChatExtensionsMessageContext]
    role: AzureChatCompletionRole  # type: ignore


class AzureChatCompletionChoice(ChatChoice):
    content_filter_results: Optional[ContentFilterResults]
    message: AzureChatCompletionMessage  # type: ignore


class AzureChatCompletion(ChatCompletion):
    choices: List[AzureChatCompletionChoice]  # type: ignore
    prompt_filter_results: Optional[List[PromptFilterResult]]


class AzureChoiceDelta(ChoiceDelta):
    context: Optional[AzureChatExtensionsMessageContext]


class AzureChatCompletionChoiceDelta(ChatChoiceDelta):
    delta: AzureChoiceDelta  # type: ignore
    content_filter_results: Optional[ContentFilterResults]


class AzureChatCompletionChunk(ChatCompletionChunk):
    choices: List[AzureChatCompletionChoiceDelta]  # type: ignore
    prompt_filter_results: Optional[List[PromptFilterResult]]


class AzureCompletionChoice(CompletionChoice):
    content_filter_results: Optional[ContentFilterResults]


class AzureCompletion(Completion):
    choices: List[AzureCompletionChoice]  # type: ignore
    prompt_filter_results: Optional[List[PromptFilterResult]]
