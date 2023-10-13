# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from azure.openai import Stream


class TestStreaming:

    def data(self):
        yield b'data: {"msg": "this is a message"}\n\ndata: [DONE]\n\n'

    def data_no_space(self):
        yield b'data:{"msg": "this is a message"}\n\ndata: [DONE]\n\n'

    def data_split_by_chunk(self):
        data = [b'data: {"msg": "this is a message ', b'that got split on multiple data lines"}\n\ndata: [DONE]\n\n']
        for d in data:
            yield d

    def test_stream_data(self):
        stream = Stream(
            return_type=lambda x: x,
            response=object(),
            iter_response=self.data(),
        )

        for s in stream:
            assert s == {"msg": "this is a message"}

    def test_stream_data_no_space(self):
        stream = Stream(
            return_type=lambda x: x,
            response=object(),
            iter_response=self.data_no_space(),
        )

        for s in stream:
            assert s == {"msg": "this is a message"}

    def test_stream_split(self):
        stream = Stream(
            return_type=lambda x: x,
            response=object(),
            iter_response=self.data_split_by_chunk(),
        )

        for s in stream:
            assert s == {"msg": "this is a message that got split on multiple data lines"}
