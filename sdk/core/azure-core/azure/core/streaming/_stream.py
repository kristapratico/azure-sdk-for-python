# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------

from typing import Iterator, TypeVar, Callable, Any, Optional, Type
from types import TracebackType

from typing_extensions import Self

from ..rest import HttpRequest, HttpResponse
from ..pipeline import PipelineResponse
from ._decoders import JSONLDecoder


ReturnType = TypeVar("ReturnType")


class Stream(Iterator[ReturnType]):
    """Stream class.

    :keyword response: The response object.
    :paramtype response: ~azure.core.pipeline.PipelineResponse
    :keyword deserialization_callback: A callback that takes HttpResponse and returns a deserialized object
    :paramtype deserialization_callback: Callable
    :keyword terminal_event: A terminal event that indicates the end of the SSE stream.
    :paramtype terminal_event: Optional[str]
    """
    def __init__(
        self,
        *,
        response: PipelineResponse[HttpRequest, HttpResponse],
        deserialization_callback: Callable[[Any, Any], ReturnType],
        decoder: Any = None,  # TODO will be a protocol
        terminal_event: Optional[str] = None,
    ) -> None:
        self._response = response.http_response
        self._deserialization_callback = deserialization_callback
        self._terminal_event = terminal_event
        self._iterator = self._iter_events()  # TODO allow user to pass in and create own iterator class, actually this should be part of the decoder

        if decoder is not None:
            self._decoder = decoder
        elif self._response.headers.get("Content-Type") == "application/jsonl":
            self._decoder = JSONLDecoder()
        else:
            raise ValueError(
                f"Unsupported Content-Type "
                f"{self._response.headers.get('Content-Type')} "
                "for streaming. Provide a decoder."
            )


    def __next__(self) -> ReturnType:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[ReturnType]:
        yield from self._iterator

    def _iter_events(self) -> Iterator[ReturnType]:
        for line in self._parse_chunk(self._response.iter_bytes()):
            for data in line.splitlines():
                if data:
                    self._decoder.decode(data)
                else:
                    event = self._decoder.event()
                    if self._terminal_event:
                        if event.data == self._terminal_event:
                            break

                    result = self._deserialization_callback(self._response, event.json())

                    yield result
        if data:
            event = self._decoder.event()
            result = self._deserialization_callback(self._response, event.json())

            yield result

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[str]:
        data = b''
        for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self._decoder.line_endings):
                    yield data.decode("utf-8")
                    data = b''
        if data:
            yield data

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        self.close()

    def __enter__(self) -> Self:
        return self

    def close(self) -> None:
        self._response.close()
