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

import httpx

from typing import Iterator, AsyncIterator, Tuple, List, Any, Optional

from ._events import JSONLEvent, ServerSentEvent


class JSONLDecoder:
    def __init__(self) -> None:
        self._data: str = ""
        self._line_separators: Tuple[bytes, ...] = (b"\n", b"\r\n")

    def decode(self, line: bytes) -> None:
        self._data = line.decode("utf-8")

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[JSONLEvent]:
        data = b''
        for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self._line_separators):
                    self.decode(data.splitlines()[0])
                    event = self.event()
                    yield event
                    data = b''

        if data:
            # the last line did not end with a line separator
            # ok per JSONL spec: https://jsonlines.org/
            self.decode(data)
            event = self.event()
            yield event

    async def aiter_events(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[JSONLEvent]:
        data = b''
        async for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self._line_separators):
                    self.decode(data.splitlines()[0])
                    event = self.event()
                    yield event
                    data = b''

        if data:
            # the last line did not end with a line separator
            # ok per JSONL spec: https://jsonlines.org/
            self.decode(data)
            event = self.event()
            yield event

    def event(self) -> JSONLEvent:
        jsonl = JSONLEvent(data=self._data)
        self._data = ""
        return jsonl


class SSEDecoder:
    def __init__(self, *, client: Optional[Any] = None, response: Optional[Any] = None) -> None:
        self._data: List[str] = []
        self._line_separators = (b'\r\r', b'\n\n', b'\r\n\r\n')
        self._last_event_id = None
        self._event = None
        self._retry = None
        self._client = client
        self._response = response

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


    async def aiter_events(self, iter_bytes: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        ...


    def _get_data(self, iter_bytes: Iterator[bytes]) -> Iterator[bytes]:
        data = b''
        for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self._line_separators):
                    yield data
                    data = b''

        if data:
            yield data

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[bytes]:

        try:
            yield self._get_data(iter_bytes)
        except httpx.ReadError:
            # TODO what will this actually raise?
            # try to reestablish the connection
            # 1. sleep the retry time / 1000
            # 2. If there is a last_event_id, add it to the request headers
            # 3. Send the request to try to reestablish the connection
            # 3.5 implement jitter/exponential backoff for retry?
            # 4. If the connection is reestablished, continue to read the stream
            # 5. If server returns 204, stop 
            if self._retry is not None:
                self._client._pipeline._transport.sleep(self._retry / 1000)
            headers = {"Accept": "text/event-stream"}
            if self._last_event_id:
                headers["Last-Event-ID"] = self._last_event_id
            response = self._client.send_request(self._response.request, headers=headers)
            yield self.iter_events(response.iter_bytes())


    def event(self) -> ServerSentEvent:
        sse = ServerSentEvent(
            event="data",
            data="\n".join(self._data),
            last_event_id=self._last_event_id,
            retry=self._retry,
        )
        self._data = []
        self._event = None
        self._retry = None
        return sse