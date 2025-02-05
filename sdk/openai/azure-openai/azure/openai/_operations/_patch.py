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

from azure.core.pipeline import PipelineResponse
from azure.core.rest import HttpRequest, HttpResponse

ReturnType = TypeVar("ReturnType")


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


class SSEDecoder:
    def __init__(self) -> None:
        self._data: List[str] = []
        self._line_separators = (b'\r\r', b'\n\n', b'\r\n\r\n')
        self._last_event_id = None
        self._event = None
        self._retry = None

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
        response: HttpResponse,
        deserialization_callback: Callable[[Any], ReturnType],
        decoder = None,
        terminal_event: Optional[str] = None,
        client: Optional[Any] = None,
    ) -> None:
        self._response = response
        self._decoder = SSEDecoder()
        self._deserialization_callback = deserialization_callback
        self._terminal_event = terminal_event
        self._iterator = self._iter_events()

    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        yield from self._iterator

    def _iter_events(self) -> Iterator[ReturnType]:
        for event in self._decoder.iter_events(self._response.iter_bytes()):
            if event.data == self._terminal_event:
                break

            result = self._deserialization_callback(event.json())
            yield result

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



__all__: List[str] = ["Stream"]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
