# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, Sequence, Optional, Mapping, overload, Union, AsyncIterable
from typing_extensions import Literal
from azure.core.tracing.decorator_async import distributed_trace_async
from ._operations import (
    EmbeddingsOperations as GeneratedEmbeddingsOperations,
    CompletionsOperations as GeneratedCompletionsOperations,
    ChatCompletionsOperations as GeneratedChatCompletionsOperations,
    ImagesOperations as GeneratedImagesOperations,
)
from ...models._enums import FunctionCallPreset, ImageSize, ImageGenerationResponseFormat
from ...models._models import (
    Embeddings,
    EmbeddingsOptions,
    Completions,
    CompletionsOptions,
    ChatCompletionsOptions,
    ChatCompletions,
    ChatMessage,
    FunctionDefinition,
    AzureChatExtensionConfiguration,
    ImageGenerationOptions,
    ImageGenerations,
)


class EmbeddingsOperations(GeneratedEmbeddingsOperations):

    @distributed_trace_async
    async def create(
        self,
        deployment_id: str,
        input: Sequence[str],
        *,
        user: Optional[str] = None,
        **kwargs
    ) -> Embeddings:
        return await super()._create(
            deployment_id=deployment_id,
            body=EmbeddingsOptions(
                input=input,
                user=user
            ),
            **kwargs
        )



class CompletionsOperations(GeneratedCompletionsOperations):

    @overload
    async def create(
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
    ) -> AsyncIterable[Completions]:
        ...

    @overload
    async def create(
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

    @distributed_trace_async
    async def create(
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
    ) -> Union[Completions, AsyncIterable[Completions]]:
        if stream:
            raise NotImplementedError("SSE not implemented")

        return await super()._create(
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
    async def create(
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
    ) -> AsyncIterable[ChatCompletions]:
        ...

    @overload
    async def create(
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

    @distributed_trace_async
    async def create(
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
    ) -> Union[ChatCompletions, AsyncIterable[ChatCompletions]]:
        if stream:
            raise NotImplementedError("SSE not implemented")

        if data_sources:
            return await super()._create_extensions(
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

        return await super()._create(
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


class ImagesOperations(GeneratedImagesOperations):

    @distributed_trace_async
    async def generate(
        self,
        prompt: str,
        *,
        n: Optional[int] = None,
        size: Optional[Union[str, ImageSize]] = None,
        response_format: Optional[Union[str, ImageGenerationResponseFormat]] = None,
        user: Optional[str] = None,
        **kwargs,
    ) -> ImageGenerations:
        poller = await super().begin__generate(  # TODO: this should generate internal https://github.com/Azure/autorest.python/issues/2070
            body=ImageGenerationOptions(
                prompt=prompt,
                n=n,
                size=size,
                response_format=response_format,
                user=user,
            ),
            **kwargs
        )
        result = await poller.result()
        return ImageGenerations(result.as_dict()["result"])


__all__: List[str] = [
    "EmbeddingsOperations",
    "CompletionsOperations",
    "ChatCompletionsOperations",
    "ImagesOperations",
]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
