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
from typing import Iterator, List, Tuple, Union

from ._events import JSONLEvent


class JSONLDecoder:
    def __init__(self) -> None:
        self.data: List[str] = []
        self.line_separators: Tuple[bytes, ...] = (b"\n", b"\r\n")

    def decode(self, line: bytes) -> None:
        data = line.decode("utf-8")
        self.data.append(data)

    def iter_events(self, iter_bytes: Iterator[bytes]) -> Iterator[JSONLEvent]:
        for line in self._parse_chunk(iter_bytes):
            if line:
                self.decode(line)

            event = self.event()
            if event:
                yield event

    def _parse_chunk(self, iter_bytes: Iterator[bytes]) -> Iterator[bytes]:
        data = b''
        for chunk in iter_bytes:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith(self.line_separators):
                    yield data
                    data = b''

        # the last line did not end with a line separator
        # ok per JSONL spec: https://jsonlines.org/
        if data:
            yield data

    def event(self) -> Union[JSONLEvent, None]:
        if not self.data:
            return
        jsonl = JSONLEvent(data="\n".join(self.data))
        self.data = []
        return jsonl
