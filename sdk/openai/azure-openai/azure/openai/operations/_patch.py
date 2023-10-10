# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, Sequence, Optional, Mapping, overload, Union, Iterable
from typing_extensions import Literal
from azure.core.tracing.decorator import distributed_trace
from ._operations import (
    EmbeddingsOperations as GeneratedEmbeddingsOperations,
    CompletionsOperations as GeneratedCompletionsOperations,
    ChatCompletionsOperations as GeneratedChatCompletionsOperations,
)
from ..models._enums import FunctionCallPreset
from ..models._models import (
    Embeddings,
    EmbeddingsOptions,
    Completions,
    CompletionsOptions,
    ChatCompletionsOptions,
    ChatCompletions,
    ChatMessage,
    FunctionDefinition,
    AzureChatExtensionConfiguration,
)


class EmbeddingsOperations(GeneratedEmbeddingsOperations):

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        input: Sequence[str],
        *,
        user: Optional[str] = None,
        **kwargs
    ) -> Embeddings:
        return super()._create(
            deployment_id=deployment_id,
            body=EmbeddingsOptions(
                input=input,
                user=user
            ),
            **kwargs
        )


class CompletionsOperations(GeneratedCompletionsOperations):

    @overload
    def create(
        self,
        deployment_id: str,
        prompt: Sequence[str],
        *,
        stream: Literal[True],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int],
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Sequence[str]],
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        best_of: Optional[int] = None,
        **kwargs
    ) -> Iterable[Completions]:
        ...

    @overload
    def create(
        self,
        deployment_id: str,
        prompt: Sequence[str],
        *,
        stream: Optional[Literal[False]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int],
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Sequence[str]],
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        best_of: Optional[int] = None,
        **kwargs
    ) -> Completions:
        ...

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        prompt: Sequence[str],
        *,
        stream: Optional[Literal[False, True]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int] = None,
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Sequence[str]] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        best_of: Optional[int] = None,
        **kwargs
    ) -> Union[Completions, Iterable[Completions]]:
        if stream:
            raise NotImplementedError("SSE not implemented")

        return super()._create(
            deployment_id=deployment_id,
            body=CompletionsOptions(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                logit_bias=logit_bias,
                user=user,
                n=n,
                logprobs=logprobs,
                echo=echo,
                stop=stop,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                best_of=best_of,
            ),
            **kwargs
        )


class ChatCompletionsOperations(GeneratedChatCompletionsOperations):
    @overload
    def create(
        self,
        deployment_id: str,
        prompt: Sequence[str],
        *,
        stream: Literal[True],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int],
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Sequence[str]],
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        best_of: Optional[int] = None,
        **kwargs
    ) -> Iterable[ChatCompletions]:
        ...

    @overload
    def create(
        self,
        deployment_id: str,
        prompt: Sequence[str],
        *,
        stream: Optional[Literal[False]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int],
        logprobs: Optional[int] = None,
        echo: Optional[bool] = None,
        stop: Optional[Sequence[str]],
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        best_of: Optional[int] = None,
        **kwargs
    ) -> ChatCompletions:
        ...

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        messages: Sequence[ChatMessage],
        *,
        stream: Optional[Literal[False, True]] = None,
        functions: Optional[Sequence[FunctionDefinition]] = None,
        function_call: Optional[Union[str, FunctionCallPreset]] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        logit_bias: Optional[Mapping[str, int]] = None,
        user: Optional[str] = None,
        n: Optional[int] = None,
        stop: Optional[Sequence[str]] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        data_sources: Sequence[AzureChatExtensionConfiguration] = None,
        **kwargs
    ) -> Union[ChatCompletions, Iterable[ChatCompletions]]:
        if stream:
            raise NotImplementedError("SSE not implemented")

        if data_sources:
            return super()._create_extensions(
                deployment_id=deployment_id,
                body=ChatCompletionsOptions(
                    messages=messages,
                    functions=functions,
                    function_call=function_call,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    logit_bias=logit_bias,
                    user=user,
                    n=n,
                    stop=stop,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                    data_sources=data_sources,
                ),
                **kwargs
            )

        return super()._create(
            deployment_id=deployment_id,
            body=ChatCompletionsOptions(
                messages=messages,
                functions=functions,
                function_call=function_call,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                logit_bias=logit_bias,
                user=user,
                n=n,
                stop=stop,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            ),
            **kwargs
        )



__all__: List[str] = [
    "EmbeddingsOperations",
    "CompletionsOperations",
    "ChatCompletionsOperations"
]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
