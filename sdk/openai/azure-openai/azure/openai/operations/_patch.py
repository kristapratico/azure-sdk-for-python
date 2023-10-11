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
    Iterable,
    IO,
    cast,
    TypeVar,
    Dict,
    Callable,
    Any,
    Generic,
    Iterator,
    AsyncIterator,
    TYPE_CHECKING
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
from azure.core.tracing.decorator import distributed_trace
from azure.core.utils import case_insensitive_dict
from ._operations import (
    EmbeddingsOperations as GeneratedEmbeddingsOperations,
    CompletionsOperations as GeneratedCompletionsOperations,
    ChatCompletionsOperations as GeneratedChatCompletionsOperations,
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
if TYPE_CHECKING:
    from .._client import OpenAIClient


def build_audio_transcriptions_request(deployment_id: str, **kwargs: Any) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

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

    # Construct headers
    # _headers["content-type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="POST", url=_url, params=_params, headers=_headers, **kwargs)


def build_audio_translations_request(deployment_id: str, **kwargs: Any) -> HttpRequest:
    _headers = case_insensitive_dict(kwargs.pop("headers", {}) or {})
    _params = case_insensitive_dict(kwargs.pop("params", {}) or {})

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

    # Construct headers
    # _headers["content-type"] = _SERIALIZER.header("content_type", content_type, "str")
    _headers["Accept"] = _SERIALIZER.header("accept", accept, "str")

    return HttpRequest(method="POST", url=_url, params=_params, headers=_headers, **kwargs)



# copied from https://github.com/florimondmanca/httpx-sse/blob/master/src/httpx_sse/_decoders.py
class ServerSentEvent:
    def __init__(
        self,
        *,
        event: str | None = None,
        data: str | None = None,
        id: str | None = None,
        retry: int | None = None,
    ) -> None:
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> str | None:
        return self._event

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def retry(self) -> int | None:
        return self._retry

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    def __init__(self) -> None:
        self._event = ""
        self._data: List[str] = []
        self._last_event_id = ""
        self._retry: Optional[int] = None
        self._join: bool = True

    def chunked(self, iterator: bytes) -> str:
        data = b''
        for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b'\r\r', b'\n\n', b'\r\n\r\n')):
                    yield data.decode("utf-8")
                    data = b''
            if data:
                self._join = False
                yield data.decode("utf-8")

    def iter(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields lines, iterate over it & yield every event encountered"""

        for chunk in self.chunked(iterator):
            for line in chunk.splitlines():
                sse = self.decode(line)
                if sse is not None:
                    yield sse

    async def aiter(self, iterator: AsyncIterator[str]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields lines, iterate over it & yield every event encountered"""
        async for line in iterator:
            line = line.rstrip("\n")
            sse = self.decode(line)
            if sse is not None:
                yield sse

    def decode(self, line: str) -> Optional[ServerSentEvent]:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data) if self._join else self._data[-1],
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None
            self._join = True
            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None


class Stream(Generic[ReturnType]):

    response: HttpResponse

    def __init__(
        self,
        *,
        return_type: type[ReturnType],
        response: HttpResponse,
    ) -> None:
        self.response = response
        self._return_type = return_type
        self._decoder = SSEDecoder()
        self._iterator = self._stream()

    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter(self.response)

    def _stream(self) -> Iterator[ReturnType]:
        return_type = self._return_type

        for sse in self._iter_events():
            if sse.data.startswith("[DONE]"):
                break

            if sse.event is None:
                yield return_type(sse.json())


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
    ) -> Union[Completions, Stream[Completions]]:
        response = super()._create(
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
            ),
            stream=stream,
            **kwargs
        )
        if stream:
            return Stream[Completions](
                return_type=Completions,
                response=response,  # TODO: what do we want response to be?
            )
        return response


class ChatCompletionsOperations(GeneratedChatCompletionsOperations):
    @overload
    def create(
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
        data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
        **kwargs
    ) -> Union[ChatCompletions, Stream[ChatCompletions]]:
        if data_sources:
            response = super()._create_extensions(
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
                **kwargs
            )
        else:
            response = super()._create(
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
                ),
                stream=stream,
                **kwargs
            )
        if stream:
            return Stream[ChatCompletions](
                return_type=ChatCompletions,
                response=response,  # TODO: what do we want response to be?
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
        **kwargs,
    ) -> ImageGenerations:
        poller = super().begin__generate(  # TODO: this should generate internal https://github.com/Azure/autorest.python/issues/2070
            body=ImageGenerationOptions(
                prompt=prompt,
                n=n,
                size=size,
                response_format=response_format,
                user=user,
            ),
            **kwargs
        )
        result = poller.result()
        return ImageGenerations(result.as_dict()["result"])


class AudioOperations(GeneratedAudioOperations):

    @overload
    def transcriptions(
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
    def transcriptions(
        self,
        deployment_id: str,
        file: bytes,
        *,
        response_format: Optional[Union[str, AudioTranscriptionFormat]] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranscription:
        ...

    @distributed_trace
    def transcriptions(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
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
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
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
    def translations(
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
    def translations(
        self,
        deployment_id: str,
        file: bytes,
        *,
        response_format: Optional[Union[str, AudioTranslationFormat]] = None,
        prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs,
    ) -> AudioTranslation:
        ...

    @distributed_trace
    def translations(
        self,
        deployment_id: str,
        file: Union[bytes, IO[bytes]],
        *,
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
        pipeline_response: PipelineResponse = self._client._pipeline.run(  # pylint: disable=protected-access
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
