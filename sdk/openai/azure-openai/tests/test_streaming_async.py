# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import pytest
from azure.openai.aio import AsyncStream



class TestStreamingAsync:
 
    async def data(self):
        yield b'data: {"msg": "this is a message"}\n\ndata: [DONE]\n\n'

    async def data_no_space(self):
        yield b'data:{"msg": "this is a message"}\n\ndata: [DONE]\n\n'

    async def data_split_by_chunk(self):
        data = [b'data: {"msg": "this is a message ', b'that got split on multiple data lines"}\n\ndata: [DONE]\n\n']
        for d in data:
            yield d

    @pytest.mark.asyncio
    async def test_stream_data_async(self):
        stream = AsyncStream(
            return_type=lambda x: x,
            response=object(),
            aiter_response=self.data(),
        )

        async for s in stream:
            assert s == {"msg": "this is a message"}

    @pytest.mark.asyncio
    async def test_stream_data_no_space_async(self):
        stream = AsyncStream(
            return_type=lambda x: x,
            response=object(),
            aiter_response=self.data_no_space(),
        )

        async for s in stream:
            assert s == {"msg": "this is a message"}

    @pytest.mark.asyncio
    async def test_stream_split_async(self):
        stream = AsyncStream(
            return_type=lambda x: x,
            response=object(),
            aiter_response=self.data_split_by_chunk(),
        )

        async for s in stream:
            assert s == {"msg": "this is a message that got split on multiple data lines"}
