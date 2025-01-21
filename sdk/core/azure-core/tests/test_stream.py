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
        for d in data:
            yield d

    def test_stream_data(self):
        stream = Stream(
            deserialization_callback=lambda _, x: x,
            response=MockPipelineResponse(MockResponse(self.multiple_data)),
            decoder=JSONLDecoder(),
        )

        for s in stream:
            assert s == {"msg": "this is a message"}

    # def test_stream_data_no_space(self):
    #     stream = Stream(
    #         return_type=lambda x: x,
    #         response=object(),
    #         iter_response=self.data_no_space(),
    #     )

    #     for s in stream:
    #         assert s == {"msg": "this is a message"}
