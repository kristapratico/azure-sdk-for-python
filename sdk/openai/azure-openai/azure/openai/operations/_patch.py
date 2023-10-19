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
    IO,
    TypeVar,
    Dict,
    Callable,
    Any,
    Generic,
    Iterator,
    AsyncIterator,
    Type,
)
from typing_extensions import Literal
from azure.core.tracing.decorator import distributed_trace
from azure.core.exceptions import (
    ClientAuthenticationError,
    HttpResponseError,
    ResourceExistsError,
    ResourceNotFoundError,
    ResourceNotModifiedError,
    map_error,
)
from azure.core.pipeline import PipelineResponse
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.utils import case_insensitive_dict
from ._operations import (
    EmbeddingsOperations as GeneratedEmbeddingsOperations,
    CompletionsOperations as GeneratedCompletionsOperations,
    ChatOperations as GeneratedChatOperations,
    ImagesOperations as GeneratedImagesOperations,
    AudioOperations as GeneratedAudioOperations,
)
from .._model_base import AzureJSONEncoder, _deserialize
from .._serialization import Serializer
from ..models._enums import (
    FunctionCallPreset,
    ImageSize,
    ImageGenerationResponseFormat,
    AudioTranscriptionFormat,
    AudioTranslationFormat,
)
from ..models._models import (
    FunctionName,
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
ClsType = Optional[Callable[[PipelineResponse[HttpRequest, HttpResponse], T, Dict[str, Any]], Any]]

_SERIALIZER = Serializer()
_SERIALIZER.client_side_validation = False

ReturnType = TypeVar("ReturnType")


def build_audio_transcriptions_request(deployment_id: str, **kwargs: Any) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    # TODO: can't pass the content-type, azure-core intentionally omits it in order
    # to let requests/aiohttp set it automatically
    # content_type: str = kwargs.pop("content_type")
    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-09-01-preview"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = "/deployments/{deploymentId}/audio/transcriptions"
    path_format_arguments = {
        "deploymentId": _SERIALIZER.url("deployment_id", deployment_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # TODO: can't pass the content-type, azure-core intentionally omits it in order
    # to let requests/aiohttp set it automatically
    # Construct headers
    # _headers["content-type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="POST", url=_url, params=_params, headers=_headers, **kwargs)


def build_audio_translations_request(deployment_id: str, **kwargs: Any) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

    # TODO: can't pass the content-type, azure-core intentionally omits it in order
    # to let requests/aiohttp set it automatically
    # content_type: str = kwargs.pop("content_type")
    api_version: str = kwargs.pop("api_version", _params.pop("api-version", "2023-09-01-preview"))
    accept = _headers.pop("Accept", "application/json")

    # Construct URL
    _url = "/deployments/{deploymentId}/audio/translations"
    path_format_arguments = {
        "deploymentId": _SERIALIZER.url("deployment_id", deployment_id, "str"),
    }

    _url: str = _url.format(**path_format_arguments)  # type: ignore

    # Construct parameters
    _params["api-version"] = _SERIALIZER.query("api_version", api_version, "str")

    # TODO: can't pass the content-type, azure-core intentionally omits it in order
    # to let requests/aiohttp set it automatically
    # Construct headers
    # _headers["content-type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="POST", url=_url, params=_params, headers=_headers, **kwargs)


# inspired from https://github.com/openai/openai-python/blob/v1/src/openai/_streaming.py
class ServerSentEvent:
    def __init__(
        self,
        *,
        data: Optional[str] = None,
    ) -> None:
        self._data = data

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"ServerSentEvent(data={self.data})"


class SSEDecoder:
    """https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation"""

    EMPTY_LINE = (b'\r\r', b'\n\n', b'\r\n\r\n')

    def __init__(self) -> None:
        self._data: List[str] = []

    def chunked(self, iterator: Iterator[bytes]) -> Iterator[str]:
        data = b''
        for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self.EMPTY_LINE):
                    yield data.decode("utf-8")
                    data = b''

    async def achunked(self, async_iterator: AsyncIterator[bytes]) -> AsyncIterator[str]:
        data = b''
        async for chunk in async_iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self.EMPTY_LINE):
                    yield data.decode("utf-8")
                    data = b''

    def iter(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        for chunk in self.chunked(iterator):
            for line in chunk.splitlines():
                sse = self.decode(line)
                if sse is not None:
                    yield sse

    async def aiter(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        async for chunk in self.achunked(iterator):
            for line in chunk.splitlines():
                sse = self.decode(line)
                if sse is not None:
                    yield sse

    def decode(self, line: str) -> Optional[ServerSentEvent]:

        if not line:
            return self.event()

        if line.startswith(":"):
            # comment, ignore the line
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            # data:test and data: test are equivalent
            value = value[1:]
        if fieldname == "data":
            self._data.append(value)
        else:
            pass  # field is ignored.

        return None

    def event(self) -> Optional[ServerSentEvent]:
        if not self._data:
            return None

        sse = ServerSentEvent(
            data="\n".join(self._data),
        )
        
        self._data = []
        return sse


class Stream(Generic[ReturnType]):

    response: HttpResponse

    def __init__(
        self,
        *,
        return_type: Type[ReturnType],
        iter_response: Iterator[bytes],
        response: HttpResponse,
    ) -> None:
        self.response = response
        self._iter_response = iter_response
        self._return_type = return_type
        self._decoder = SSEDecoder()
        self._iterator = self._stream()

    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter(self._iter_response)

    def _stream(self) -> Iterator[ReturnType]:
        for sse in self._iter_events():
            if sse.data.startswith("[DONE]"):
                break

            yield self._return_type(sse.json())


class EmbeddingsOperations(GeneratedEmbeddingsOperations):

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        input: Sequence[str],
        *,
        user: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Embeddings:
        return super()._create(
            deployment_id=deployment_id,
            body=EmbeddingsOptions(
                input=input,
                user=user,
                model=model,
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
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Stream[Completions]:
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
        model: Optional[str] = None,
        **kwargs: Any
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
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Union[Completions, Stream[Completions]]:
        response, pipeline_response = super()._create(
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
                stream=stream,
                model=model,
            ),
            stream=stream,
            cls=lambda pipeline_response, deserialized, _: (deserialized, pipeline_response),
            **kwargs
        )
        if stream:
            return Stream[Completions](
                return_type=Completions,
                response=pipeline_response.http_response,
                iter_response=response,
            )
        return response


class ChatOperations(GeneratedChatOperations):

    completions: "ChatCompletionsOperations"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.completions = ChatCompletionsOperations(*args, **kwargs)


class ChatCompletionsOperations(GeneratedChatOperations):

    @overload
    def create(
        self,
        deployment_id: str,
        messages: Sequence[ChatMessage],
        *,
        stream: Literal[True],
        functions: Optional[Sequence[FunctionDefinition]] = None,
        function_call: Optional[Union[str, FunctionCallPreset, FunctionName]] = None,
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
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Stream[ChatCompletions]:
        ...

    @overload
    def create(
        self,
        deployment_id: str,
        messages: Sequence[ChatMessage],
        *,
        stream: Optional[Literal[False]] = None,
        functions: Optional[Sequence[FunctionDefinition]] = None,
        function_call: Optional[Union[str, FunctionCallPreset, FunctionName]] = None,
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
        model: Optional[str] = None,
        **kwargs: Any
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
        function_call: Optional[Union[str, FunctionCallPreset, FunctionName]] = None,
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
        model: Optional[str] = None,
        **kwargs: Any
    ) -> Union[ChatCompletions, Stream[ChatCompletions]]:
        if data_sources:
            response, pipeline_response = super()._create_extensions(
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
                    stream=stream,
                ),
                stream=stream,
                cls=lambda pipeline_response, deserialized, _: (deserialized, pipeline_response),
                **kwargs
            )
        else:
            response, pipeline_response = super()._create(
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
                    stream=stream,
                    model=model,
                ),
                stream=stream,
                cls=lambda pipeline_response, deserialized, _: (deserialized, pipeline_response),
                **kwargs
            )
        if stream:
            return Stream[ChatCompletions](
                return_type=ChatCompletions,
                response=pipeline_response.http_response,
                iter_response=response,
            )
        return response


class ImagesOperations(GeneratedImagesOperations):

    @distributed_trace
    def generate(
        self,
        prompt: str,
        *,
        n: Optional[int] = None,
        size: Optional[Union[str, ImageSize]] = None,
        response_format: Optional[Union[str, ImageGenerationResponseFormat]] = None,
        user: Optional[str] = None,
        **kwargs: Any,
    ) -> ImageGenerations:
        try:
            poller = super()._begin_generate(
                body=ImageGenerationOptions(
                    prompt=prompt,
                    n=n,
                    size=size,
                    response_format=response_format,
                    user=user,
                ),
                **kwargs
            )
        except HttpResponseError as e:
            if e.status_code == 200:
                # non-azure openai caller
                return ImageGenerations(e.response.json())
            raise e
        result = poller.result()
        return ImageGenerations(result.as_dict()["result"])


class AudioOperations(GeneratedAudioOperations):

    transcriptions: "TranscriptionsOperations"
    translations: "TranslationsOperations"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.transcriptions = TranscriptionsOperations(*args, **kwargs)
        self.translations = TranslationsOperations(*args, **kwargs)


class TranscriptionsOperations(GeneratedAudioOperations):

    @overload
    def create(
        self,
        deployment_id: str,
        file: IO[bytes],
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranscription:
        ...

    @overload
    def create(
        self,
        deployment_id: str,
        file: bytes,
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranscription:
        ...

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranscription:

        data = {
            "response_format": response_format,
            "language": language,
            "prompt": prompt,
            "temperature": temperature,
            "model": model
        }

        if hasattr(file, "name"):
            filename = file.name
        else:
            filename = "filename.mp3"

        files={"file": (filename, file, "application/octet-stream")}

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        # TODO: can't pass the content-type, azure-core intentionally omits it in order
        # to let requests/aiohttp set it automatically
        # content_type: str = kwargs.pop("content_type", _headers.pop("content-type", "multipart/form-data"))
        cls: ClsType[AudioTranscription] = kwargs.pop("cls", None)  # pylint: disable=protected-access

        # TODO I need data as a dictionary, not a JSON string
        _data = json.loads(json.dumps(data, cls=AzureJSONEncoder, exclude_readonly=True))  # type: ignore

        request = build_audio_transcriptions_request(
            deployment_id=deployment_id,
            api_version=self._config.api_version,
            data=_data,
            headers=_headers,
            params=_params,
            files=files
        )
        # TODO: set_multipart_body in azure-core breaks files, need to reset it here
        request._files = files  # pylint: disable=protected-access
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        _stream = kwargs.pop("stream", False)
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        # TODO Certain response formats return text, not JSON
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


class TranslationsOperations(GeneratedAudioOperations):

    @overload
    def create(
        self,
        deployment_id: str,
        file: IO[bytes],
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranslation:
        ...

    @overload
    def create(
        self,
        deployment_id: str,
        file: bytes,
        *,
        response_format: Optional[Union[str, AudioTranslationFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranslation:
        ...

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
        response_format: Optional[Union[str, AudioTranslationFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AudioTranslation:

        data = {
            "response_format": response_format,
            "prompt": prompt,
            "temperature": temperature,
            "model": model,
        }

        if hasattr(file, "name"):
            filename = file.name
        else:
            filename = "filename.mp3"

        files={"file": (filename, file, "application/octet-stream")}

        error_map = {
            401: ClientAuthenticationError,
            404: ResourceNotFoundError,
            409: ResourceExistsError,
            304: ResourceNotModifiedError,
        }
        error_map.update(kwargs.pop("error_map", {}) or {})

        _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
        _params = kwargs.pop("params", {}) or {}

        # TODO: can't pass the content-type, azure-core intentionally omits it in order
        # to let requests/aiohttp set it automatically
        # content_type: str = kwargs.pop("content_type", _headers.pop("content-type", "multipart/form-data"))
        cls: ClsType[AudioTranslation] = kwargs.pop("cls", None)  # pylint: disable=protected-access

        # TODO I need data as a dictionary, not a JSON string
        _data = json.loads(json.dumps(data, cls=AzureJSONEncoder, exclude_readonly=True))  # type: ignore

        request = build_audio_translations_request(
            deployment_id=deployment_id,
            api_version=self._config.api_version,
            data=_data,
            headers=_headers,
            params=_params,
            files=files
        )
        # TODO: set_multipart_body in azure-core breaks files, need to reset it here
        request._files = files  # pylint: disable=protected-access
        path_format_arguments = {
            "endpoint": self._serialize.url("self._config.endpoint", self._config.endpoint, "str", skip_quote=True),
        }
        request.url = self._client.format_url(request.url, **path_format_arguments)

        _stream = kwargs.pop("stream", False)
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
            request, stream=_stream, **kwargs
        )

        response = pipeline_response.http_response

        if response.status_code not in [200]:
            if _stream:
                response.read()  # Load the body in memory and close the socket
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)

        # TODO Certain response formats return text, not JSON
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
    "ChatOperations",
    "ChatCompletionsOperations",
    "ImagesOperations",
    "AudioOperations",
    "TranscriptionsOperations",
    "TranslationsOperations",
]


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
