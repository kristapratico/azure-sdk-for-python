# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from __future__ import annotations
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
from typing_extensions import Literal, Self
from types import TracebackType
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


class JSONLEvent:
    def __init__(
        self,
        *,
        data: Optional[str] = None,
    ) -> None:
        self.data = data
        self.event = None

    def json(self) -> Any:
        return json.loads(self.data)


class JSONLDecoder:
    def __init__(self) -> None:
        self._data: list[str] = []

    def decode(self, line: str) -> None:
        self._data.append(line)

    def event(self) -> JSONLEvent:
        jsonl = JSONLEvent(data="\n".join(self._data))
        self._data = []
        return jsonl



class ChunkIterator(Iterator[ReturnType]):
    def __init__(
        self,
        *,
        iter_bytes: Iterator[bytes],
        deserialization_callback: Callable[[Any], ReturnType],
        response: PipelineResponse,
        decoder: SSEDecoder | JSONLDecoder,
        event_mapping: Optional[Mapping[str, Type[ReturnType]]] = None,
        event_handler: Optional[Any] = None,
    ):
        self._iter_bytes = iter_bytes
        self._decoder = decoder
        self._deserialization_callback = deserialization_callback
        self._iterator = self.__iter__()
        self._callbacks = {}
        self._event_handler = event_handler
        self._event_mapping = event_mapping
        self._response = response

    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        for line in self._parse_chunk(self._iter_bytes):
            for data in line.splitlines():
                if data:
                    self._decoder.decode(data)
                else:
                    event = self._decoder.event()
                    if event.data.startswith("[DONE]"):
                        break

                    return_cls = self._deserialization_callback(self._response, event.json())
                    if event.event in self._callbacks:
                        self._callbacks[event.event](return_cls)

                    if self._event_handler:
                        getattr(self._event_handler, f"on_{event.event}")(return_cls)
                    yield return_cls

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[str]:
        data = b''
        for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b'\r\r', b'\n\n', b'\r\n\r\n')):
                    yield data.decode("utf-8")
                    data = b''


# class Stream(Iterator[ReturnType]):
#     """Stream class.

#     :param response: The response object.
#     :type response: ~azure.core.rest.HttpResponse
#     :param return_cls: The type returned by the stream. Can be a single type or a Union of types.
#     :type return_cls: Type[ReturnType]
#     :param decoder: The decoder to use to parse the stream.
#     :type decoder: Union[SSEDecoder, JSONLDecoder]
#     :param event_mapping: A mapping of event types to types to return when the event is received.
#     :type event_mapping: Optional[Mapping[str, Type[ReturnType]]]
#     :param event_handler: An event handler to call when an event is received.
#     :type event_handler: Optional[Any]
#     """
#     def __init__(
#         self,
#         *,
#         response: HttpResponse,
#         deserialization_callback: Callable[[Any], ReturnType],
#         decoder: SSEDecoder | JSONLDecoder,
#         event_mapping: Optional[Mapping[str, Type[ReturnType]]] = None,
#         event_handler: Optional[Any] = None,
#     ) -> None:
#         self._response = response
#         self._iterator = ChunkIterator[ReturnType](
#             iter_bytes=self._response.iter_bytes(),
#             deserialization_callback=deserialization_callback,
#             decoder=decoder,
#             event_handler=event_handler,
#             event_mapping=event_mapping,
#         )

#     def iter_events(self) -> None:
#         for _ in self._iterator:
#             pass

#     def register_event(self, event_type: str, on_event: Callable) -> None:
#         self._iterator._callbacks[event_type] = on_event

#     def __iter__(self) -> Iterator[ReturnType]:
#         return self

#     def __next__(self) -> ReturnType:
#         return self._iterator.__next__()

#     def __exit__(
#         self,
#         exc_type: type[BaseException] | None,
#         exc: BaseException | None,
#         exc_tb: TracebackType | None,
#     ) -> None:
#         self.close()

#     def __enter__(self) -> Self:
#         return self

#     def close(self) -> None:
#         self._response.close()




class ServerSentEvent:
    def __init__(
        self,
        *,
        data: Optional[str] = None,
        event: Optional[str] = None,
        id: Optional[str] = None,
        retry: Optional[int] = None,
    ) -> None:
        self.data = data
        self.event = event
        self.id = id
        self.retry = retry

    def json(self) -> Any:
        return json.loads(self.data)


# class SSEDecoder:
#     def __init__(self) -> None:
#         self._data: list[str] = []
#         self._last_event_id = None
#         self._event = None
#         self._retry = None

#     def decode(self, line: str) -> None:
#         if line.startswith(":"):
#             # comment, ignore the line
#             return None

#         if ":" in line:
#             field, _, value = line.partition(":")
#             if value.startswith(" "):
#                 # data:test and data: test are equivalent
#                 value = value[1:]
#         else:
#             field = line
#             value = ""

#         if field == "data":
#             self._data.append(value)
#         elif field == "event":
#             self._event = value
#         elif field == "id":
#             if "\0" in value:
#                 pass
#             else:
#                 self._last_event_id = value
#         elif field == "retry":
#             try:
#                 self._retry = int(value)
#             except (TypeError, ValueError):
#                 pass

#         # else: ignore the field

#     def event(self) -> ServerSentEvent:
#         sse = ServerSentEvent(
#             event="data",
#             data="\n".join(self._data),
#             id=self._last_event_id,
#             retry=self._retry,
#         )
        
#         self._data = []
#         self._event = None
#         self._retry = None
#         return sse



class SSEDecoder:
    def __init__(self) -> None:
        self._data: List[str] = []
        self._line_separators = (b'\r\r', b'\n\n', b'\r\n\r\n')
        self._last_event_id = None
        self._event = None
        self._retry = None
        self.counter = 0

    def decode(self, line: bytes) -> None:
        line = line.decode("utf-8")
        if line.startswith(":"):
            # comment, ignore the line
            return None

        if ":" in line:
            field, _, value = line.partition(":")
            if value.startswith(" "):
                # data:test and data: test are equivalent
                value = value[1:]
        else:
            field = line
            value = ""

        if field == "data":
            self._data.append(value)
        elif field == "event":
            self._event = value
        elif field == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif field == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass

        # else: ignore the field

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        for line in self._parse_chunk(iter_bytes):
            for data in line.splitlines():
                if data:
                    self.decode(data)
                else:
                    event = self.event()
                    yield event

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[bytes]:
        data = b''
        for chunk in iter_bytes:
            # randomly throw a TypeError to test retry
            import random
            if random.randint(0, 1) == 1:
                self.counter += 1
                if self.counter == 2 or self.counter == 4:
                    raise TypeError
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self._line_separators):
                    yield data
                    data = b''
        if data:
            yield data

    def event(self) -> ServerSentEvent:
        sse = ServerSentEvent(
            event="data",
            data="\n".join(self._data),
            id=self._last_event_id,
            retry=self._retry,
        )
        self._data = []
        self._event = None
        self._retry = None
        return sse



class Stream(Iterator[ReturnType]):
    """Stream class.

    :param response: The response object.
    :type response: ~azure.core.rest.HttpResponse
    :param return_cls: The type returned by the stream. Can be a single type or a Union of types.
    :type return_cls: Type[ReturnType]
    :param decoder: The decoder to use to parse the stream.
    :type decoder: Union[SSEDecoder, JSONLDecoder]
    """
    def __init__(
        self,
        *,
        response: PipelineResponse[HttpRequest, HttpResponse],
        deserialization_callback: Callable[[Any, Any], ReturnType], # TODO type hint correct?
        decoder = None,
        terminal_event: Optional[str] = None,
        client: Optional[Any] = None,
    ) -> None:
        self._initial_response = response
        self._response = response.http_response
        self._decoder = SSEDecoder() if self._response.headers.get("Content-Type") == "text/event-stream" else JSONLDecoder()
        self._deserialization_callback = deserialization_callback
        self._terminal_event = terminal_event
        self._client = client
        self._iterator = self._iter_events()

    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        yield from self._iterator

    def _iter_events(self) -> Iterator[ReturnType]:
        try:
            for event in self._decoder.iter_events(self._response.iter_bytes()):
                if event.data == self._terminal_event:
                    break

                result = self._deserialization_callback(self._response, event.json())
                yield result
        except TypeError: # TODO: TypeError used to simulate retry, fix to actual exception
            # only SSE streams should retry
            if isinstance(self._decoder, SSEDecoder) and self._client:
                yield from self._retry()
            else:
                raise

    def _retry(self):
        if self._decoder._retry is not None:
            self._client._pipeline._transport.sleep(self._decoder._retry / 1000)
        headers = {"Accept": "text/event-stream"}
        if self._decoder._last_event_id:
            headers["Last-Event-ID"] = self._decoder._last_event_id
        self._response = self._client.send_request(self._initial_response.http_request, headers=headers, stream=True)
        if self._response.status_code == 204:
            # server says stop trying to connect
            return
        yield from self._iter_events()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def __enter__(self) -> Self:
        return self

    def close(self) -> None:
        self._response.close()



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


class ChannelEvent:
    kind: str

class UserConnect(ChannelEvent):
    kind: Literal["userconnect"]
    username: str
    time: str

class UserMessage(ChannelEvent):
    kind: Literal["usermessage"]
    username: str
    time: str
    text: str

class UserDisconnect(ChannelEvent):
    kind: Literal["userdisconnect"]
    username: str
    time: str

ChannelEvents = Union[UserConnect, UserMessage, UserDisconnect]


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
    ) -> Stream[ChannelEvents]:
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
    ) -> ChannelEvents:
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
    ) -> Union[ChannelEvents, Stream[ChannelEvents]]:
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
        deserialization_callback = lambda pipeline_response, deserialized, _: (deserialized, pipeline_response)
        if stream:
            return Stream[ChannelEvents](
                deserialization_callback=Completions,
                response=pipeline_response.http_response,
            )
        return response


class ChatOperations(GeneratedChatOperations):

    completions: "ChatCompletionsOperations"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.completions = ChatCompletionsOperations(*args, **kwargs)


class ChatCompletionsOperations(GeneratedChatOperations):

    # @overload
    # def create(
    #     self,
    #     deployment_id: str,
    #     messages: Sequence[ChatMessage],
    #     *,
    #     stream: Literal[True],
    #     functions: Optional[Sequence[FunctionDefinition]] = None,
    #     function_call: Optional[Union[str, FunctionCallPreset, FunctionName]] = None,
    #     max_tokens: Optional[int] = None,
    #     temperature: Optional[float] = None,
    #     top_p: Optional[float] = None,
    #     logit_bias: Optional[Mapping[str, int]] = None,
    #     user: Optional[str] = None,
    #     n: Optional[int] = None,
    #     stop: Optional[Sequence[str]] = None,
    #     presence_penalty: Optional[float] = None,
    #     frequency_penalty: Optional[float] = None,
    #     data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
    #     model: Optional[str] = None,
    #     **kwargs: Any
    # ) -> Stream[ChatCompletions]:
    #     ...

    # @overload
    # def create(
    #     self,
    #     deployment_id: str,
    #     messages: Sequence[ChatMessage],
    #     *,
    #     stream: Optional[Literal[False]] = None,
    #     functions: Optional[Sequence[FunctionDefinition]] = None,
    #     function_call: Optional[Union[str, FunctionCallPreset, FunctionName]] = None,
    #     max_tokens: Optional[int] = None,
    #     temperature: Optional[float] = None,
    #     top_p: Optional[float] = None,
    #     logit_bias: Optional[Mapping[str, int]] = None,
    #     user: Optional[str] = None,
    #     n: Optional[int] = None,
    #     stop: Optional[Sequence[str]] = None,
    #     presence_penalty: Optional[float] = None,
    #     frequency_penalty: Optional[float] = None,
    #     data_sources: Optional[Sequence[AzureChatExtensionConfiguration]] = None,
    #     model: Optional[str] = None,
    #     **kwargs: Any
    # ) -> ChatCompletions:
    #     ...

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
    ) -> Stream[ChatCompletions]:
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
        cls = kwargs.pop("cls", None)

        def callback(pipeline_response, json):
            deserialized = _deserialize(ChatCompletions, json)
            if cls:
                return cls(pipeline_response, deserialized, {})
            return deserialized

        if stream:
            return Stream[ChatCompletions](
                deserialization_callback=callback,
                response=pipeline_response,
                terminal_event="[DONE]",
                client=self._client,
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
