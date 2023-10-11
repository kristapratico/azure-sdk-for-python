# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
import json
import sys
from typing import (
    List,
    Sequence,
    Optional,
    Mapping,
    overload,
    Union,
    AsyncIterable,
    IO,
    cast,
    TypeVar,
    Dict,
    Callable,
    Any
)
from typing_extensions import Literal
from azure.core.tracing.decorator_async import distributed_trace_async
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import HttpRequest, AsyncHttpResponse
from azure.core.utils import case_insensitive_dict
from ..._model_base import AzureJSONEncoder, _deserialize
from ..._serialization import Serializer
from ...operations._patch import build_audio_transcriptions_request, build_audio_translations_request
from ._operations import (
    EmbeddingsOperations as GeneratedEmbeddingsOperations,
    CompletionsOperations as GeneratedCompletionsOperations,
    ChatCompletionsOperations as GeneratedChatCompletionsOperations,
    ImagesOperations as GeneratedImagesOperations,
    AudioOperations as GeneratedAudioOperations,
)
from ...models._enums import (
    FunctionCallPreset,
    ImageSize,
    ImageGenerationResponseFormat,
    AudioTranscriptionFormat,
    AudioTranslationFormat,
)
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
    AudioTranscription,
    AudioTranslation,
)

if sys.version_info >= (3, 9):
    from collections.abc import MutableMapping
else:
    from typing import MutableMapping  # type: ignore  # pylint: disable=ungrouped-imports
JSON = MutableMapping[str, Any]  # pylint: disable=unsubscriptable-object
T = TypeVar("T")
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, AsyncHttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False


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
        messages: Sequence[ChatMessage],
        *,
        stream: Literal[True],
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
        data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
        **kwargs
    ) -> AsyncIterable[ChatCompletions]:
        ...

    @overload
    async def create(
        self,
        deployment_id: str,
        messages: Sequence[ChatMessage],
        *,
        stream: Optional[Literal[False]] = None,
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
        data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
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
        data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
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


class AudioOperations(GeneratedAudioOperations):

    @overload
    async def transcriptions(
        self,
        deployment_id: str,
        file: IO[bytes],
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranscription:
        ...

    @overload
    async def transcriptions(
        self,
        deployment_id: str,
        file: bytes,
        *,
        filename: str,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranscription:
        ...

    @distributed_trace_async
    async def transcriptions(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
        filename: Optional[str] = None,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranscription:

        data = {
            "response_format": response_format,
            "language": language,
            "prompt": prompt,
            "temperature": temperature,
        }

        files={"file": (filename or file.name, file, "application/octet-stream")}

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        # content_type: str = kwargs.pop("content_type", _headers.pop("content-type", "multipart/form-data"))
        cls: ClsType[AudioTranscription] = kwargs.pop("cls", None)  # pylint: disable=protected-access

        _data = json.loads(json.dumps(data, cls=AzureJSONEncoder, exclude_readonly=True))  # type: ignore

        request = build_audio_transcriptions_request(
            deployment_id=deployment_id,
            api_version=self._config.api_version,
            data=_data,
            headers=_headers,
            params=_params,
            files=files
        )
        request._files = files  # set_multipart_body in azure-core breaks files, need to reset it here
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        _stream = kwargs.pop("stream", False)
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if response_format in ["text", "srt", "vtt"]:
            text = response.content.decode()
            return AudioTranscription({"text": text})
        if _stream:
            deserialized = response.iter_bytes()
        else:
            deserialized = _deserialize(
                AudioTranscription, response.json()
            )

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore

    @overload
    async def translations(
        self,
        deployment_id: str,
        file: IO[bytes],
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranslation:
        ...

    @overload
    async def translations(
        self,
        deployment_id: str,
        file: bytes,
        *,
        filename: str,
        response_format: Optional[Union[str, AudioTranslationFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranslation:
        ...

    @distributed_trace_async
    async def translations(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
        filename: Optional[str] = None,
        response_format: Optional[Union[str, AudioTranslationFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranslation:

        data = {
            "response_format": response_format,
            "prompt": prompt,
            "temperature": temperature,
        }

        files={"file": (filename or file.name, file, "application/octet-stream")}

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        # content_type: str = kwargs.pop("content_type", _headers.pop("content-type", "multipart/form-data"))
        cls: ClsType[AudioTranslation] = kwargs.pop("cls", None)  # pylint: disable=protected-access

        _data = json.loads(json.dumps(data, cls=AzureJSONEncoder, exclude_readonly=True))  # type: ignore

        request = build_audio_translations_request(
            deployment_id=deployment_id,
            api_version=self._config.api_version,
            data=_data,
            headers=_headers,
            params=_params,
            files=files
        )
        request._files = files  # set_multipart_body in azure-core breaks files, need to reset it here
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        _stream = kwargs.pop("stream", False)
        pipeline_response: PipelineResponse = await self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        if response_format in ["text", "srt", "vtt"]:
            text = response.content.decode()
            return AudioTranslation({"text": text})
        if _stream:
            deserialized = response.iter_bytes()
        else:
            deserialized = _deserialize(
                AudioTranslation, response.json()
            )

        if cls:
            return cls(pipeline_response, deserialized, {})  # type: ignore

        return deserialized  # type: ignore



__all__: List[str] = [
    "EmbeddingsOperations",
    "CompletionsOperations",
    "ChatCompletionsOperations",
    "ImagesOperations",
    "AudioOperations",
]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
