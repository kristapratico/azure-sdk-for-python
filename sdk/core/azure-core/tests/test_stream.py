from azure.core.streaming import Stream
from azure.core.streaming._decoders import JSONLDecoder


class MockResponse:
    def __init__(self, iter_bytes):
        self.iter_bytes = iter_bytes


class MockPipelineResponse:
    def __init__(self, http_response):
        self.http_response = http_response


class TestStreaming:

    def data(self):
        yield b'{"msg": "this is a message"}\n'

    def multiple_data(self):
        data = [b'{"msg": "this is a message"}\n', b'{"msg": "this is another message"}\n', b'{"msg": "this is a third message"}\n{"msg": "this is a fouth message"}']
        yield from data

    def broken_up_data(self):
        data = [b'{"msg": "this is a third message"}\n{"msg": ', b'"this is a fouth message"}']
        yield from data

    def test_stream_data(self):
        stream = Stream(
            deserialization_callback=lambda _, x: x,
            response=MockPipelineResponse(MockResponse(self.data)),
            decoder=JSONLDecoder(),
        )

        for s in stream:
            assert s == {"msg": "this is a message"}

    def test_stream_multiple_data(self):
        stream = Stream(
            deserialization_callback=lambda _, x: x,
            response=MockPipelineResponse(MockResponse(self.multiple_data)),
            decoder=JSONLDecoder(),
        )
        messages = []
        for s in stream:
            messages.append(s)
        assert messages == [
            {"msg": "this is a message"},
            {"msg": "this is another message"},
            {"msg": "this is a third message"},
            {"msg": "this is a fouth message"},
        ]

    def test_stream_broken_up_data(self):
        stream = Stream(
            deserialization_callback=lambda _, x: x,
            response=MockPipelineResponse(MockResponse(self.broken_up_data)),
            decoder=JSONLDecoder(),
        )

        messages = []
        for s in stream:
            messages.append(s)
        assert messages == [
            {"msg": "this is a third message"},
            {"msg": "this is a fouth message"},
        ]

    def test_stream_next(self):
        stream = Stream(
            deserialization_callback=lambda _, x: x,
            response=MockPipelineResponse(MockResponse(self.multiple_data)),
            decoder=JSONLDecoder(),
        )
        message = next(stream)
        assert message == {"msg": "this is a message"}
        message = next(stream)
        assert message == {"msg": "this is another message"}
        message = next(stream)
        assert message == {"msg": "this is a third message"}
        message = next(stream)
        assert message == {"msg": "this is a fouth message"}
