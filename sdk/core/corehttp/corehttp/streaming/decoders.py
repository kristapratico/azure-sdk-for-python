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

import re
import codecs
from typing import Iterator, AsyncIterator, Protocol, List

from typing_extensions import runtime_checkable

from .events import JSONLEvent, ServerSentEvent, EventType


@runtime_checkable
class StreamDecoder(Protocol):
    """Protocol for stream decoders."""

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[EventType]:
        """Iterate over events from a byte iterator.

        :param iter_bytes: An iterator of byte chunks.
        :type iter_bytes: Iterator[bytes]
        :return: An iterator of events.
        """
        ...

    def event(self) -> EventType:
        """Get the current event.

        :rtype: EventType
        :return: The current event.
        """
        ...


@runtime_checkable
class AsyncStreamDecoder(Protocol):
    """Protocol for async stream decoders."""

    # Why this isn't async def: https://mypy.readthedocs.io/en/stable/more_types.html#asynchronous-iterators
    def aiter_events(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[EventType]:
        """Asynchronously iterate over events from a byte iterator.

        :param iter_bytes: An asynchronous iterator of byte chunks.
        :type iter_bytes: AsyncIterator[bytes]
        :return: An asynchronous iterator of events.
        """
        ...

    def event(self) -> EventType:
        """Get the current event.

        :return: The current event.
        """
        ...


class JSONLDecoder:
    """Decoder for JSON Lines (JSONL) format. https://jsonlines.org/"""

    def __init__(self) -> None:
        self._data: str = ""
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._line_separators = re.compile(r"\r\n|\n")

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[JSONLEvent]:
        """Iterate over JSONL events from a byte iterator.

        :param iter_bytes: An iterator of byte chunks.
        :type iter_bytes: Iterator[bytes]
        :rtype: Iterator[JSONLEvent]
        :return: An iterator of JSONLEvent objects.
        """
        buffer = ""
        for chunk in iter_bytes:
            buffer += self._decoder.decode(chunk)
            while True:
                match = self._line_separators.search(buffer)
                if match:
                    self._data = buffer[: match.start()]
                    yield self.event()
                    buffer = buffer[match.end() :]
                else:
                    break

        buffer += self._decoder.decode(b"", final=True)
        if buffer:
            # the last line did not end with a line separator
            # ok per JSONL spec
            self._data = buffer
            yield self.event()

    def event(self) -> JSONLEvent:
        """Get the current event.

        :rtype: JSONLEvent
        :return: The current event.
        """
        jsonl = JSONLEvent(data=self._data)
        self._data = ""
        return jsonl


class AsyncJSONLDecoder:
    """Asynchronous decoder for JSON Lines (JSONL) format. https://jsonlines.org/"""

    def __init__(self) -> None:
        self._data: str = ""
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._line_separators = re.compile(r"\r\n|\n")

    async def aiter_events(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[JSONLEvent]:
        """Asynchronously iterate over JSONL events from a byte iterator.

        :param iter_bytes: An asynchronous iterator of byte chunks.
        :type iter_bytes: AsyncIterator[bytes]
        :rtype: AsyncIterator[JSONLEvent]
        :return: An asynchronous iterator of JSONLEvent objects.
        """
        buffer = ""
        async for chunk in iter_bytes:
            buffer += self._decoder.decode(chunk)
            while True:
                match = self._line_separators.search(buffer)
                if match:
                    self._data = buffer[: match.start()]
                    yield self.event()
                    buffer = buffer[match.end() :]
                else:
                    break

        buffer += self._decoder.decode(b"", final=True)
        if buffer:
            # the last line did not end with a line separator
            # ok per JSONL spec
            self._data = buffer
            yield self.event()

    def event(self) -> JSONLEvent:
        """Get the current event.

        :rtype: JSONLEvent
        :return: The current event.
        """
        jsonl = JSONLEvent(data=self._data)
        self._data = ""
        return jsonl


class SSEDecoder:
    def __init__(self) -> None:
        self._data: List[str] = []
        self._last_event_id = None
        self._event_type = None
        self._retry = None
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._line_separators = re.compile(r"\r\n\r\n|\n\n|\r\r")

    def _parse_line(self, line: str) -> None:
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
            self._event_type = value
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

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[str]:
        buffer = ""
        for chunk in iter_bytes:
            buffer += self._decoder.decode(chunk)
            while True:
                match = self._line_separators.search(buffer)
                if match:
                    data = buffer[: match.end()]
                    yield data
                    buffer = buffer[match.end() :]
                else:
                    break

        buffer += self._decoder.decode(b"", final=True)
        if buffer:
            yield buffer

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        for data in self._parse_chunk(iter_bytes):
            for line in data.splitlines():
                if line:
                    self._parse_line(line)
                else:
                    event = self.event()
                    yield event

    def event(self) -> ServerSentEvent:
        sse = ServerSentEvent(
            data="\n".join(self._data),
            event_type=self._event_type or "message",
            last_event_id=self._last_event_id,
            retry=self._retry,
        )
        self._data = []
        self._event_type = None
        self._retry = None
        return sse


class AsyncSSEDecoder:
    def __init__(self) -> None:
        self._data: List[str] = []
        self._last_event_id = None
        self._event_type = None
        self._retry = None
        self._decoder = codecs.getincrementaldecoder("utf-8")()
        self._line_separators = re.compile(r"\r\n\r\n|\n\n|\r\r")

    def _parse_line(self, line: str) -> None:
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
            self._event_type = value
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

    async def _parse_chunk(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[str]:
        buffer = ""
        async for chunk in iter_bytes:
            buffer += self._decoder.decode(chunk)
            while True:
                match = self._line_separators.search(buffer)
                if match:
                    data = buffer[: match.end()]
                    yield data
                    buffer = buffer[match.end() :]
                else:
                    break

        buffer += self._decoder.decode(b"", final=True)
        if buffer:
            yield buffer

    async def aiter_events(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        async for data in self._parse_chunk(iter_bytes):
            for line in data.splitlines():
                if line:
                    self._parse_line(line)
                else:
                    event = self.event()
                    yield event

    def event(self) -> ServerSentEvent:
        sse = ServerSentEvent(
            data="\n".join(self._data),
            event_type=self._event_type or "message",
            last_event_id=self._last_event_id,
            retry=self._retry,
        )
        self._data = []
        self._event_type = None
        self._retry = None
        return sse
