import json
import asyncio
from azure.core.pipeline.policies import SansIOHTTPPolicy, HTTPPolicy, AsyncHTTPPolicy


class CognitiveServicesCredentialPolicy(SansIOHTTPPolicy):

    def __init__(self, cognitiveservices_key, **kwargs):
        if cognitiveservices_key is None:
            raise ValueError("Parameter 'credential' must not be None.")
        self.cognitiveservices_key = cognitiveservices_key
        super(CognitiveServicesCredentialPolicy, self).__init__()

    def on_request(self, request):
        request.http_request.headers["Ocp-Apim-Subscription-Key"] = self.cognitiveservices_key
        request.http_request.headers["X-BingApis-SDK-Client"] = "Python-SDK"


class ComputerVisionResponseHook(HTTPPolicy):

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        self._response_callback = kwargs.get('raw_response_hook')
        super(ComputerVisionResponseHook, self).__init__()

    def send(self, request, **kwargs):
        if request.context.options.get('response_hook', self._response_callback):
            metadata = request.context.get("metadata") or \
                request.context.options.pop("metadata", None)
            request_id = request.context.get("request_id") or \
                request.context.options.pop("request_id", None)
            response_callback = request.context.get('response_callback') or \
                request.context.options.pop('response_hook', self._response_callback)

            response = self.next.send(request)
            if metadata is None and request_id is None:
                data = json.loads(response.http_response.internal_response.text)
                request_id = data['requestId']
                metadata = data['metadata']
            for pipeline_obj in [request, response]:
                pipeline_obj.metadata = metadata
                pipeline_obj.request_id = request_id
            if response_callback:
                response_callback(response)
                request.context.response_callback = response_callback
            return response
        return self.next.send(request)


class AsyncComputerVisionResponseHook(AsyncHTTPPolicy):
    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        self._response_callback = kwargs.get('raw_response_hook')
        super(AsyncComputerVisionResponseHook, self).__init__()

    async def send(self, request, **kwargs):
        if request.context.options.get('response_hook', self._response_callback):
            metadata = request.context.get("metadata") or \
                request.context.options.pop("metadata", None)
            request_id = request.context.get("request_id") or \
                request.context.options.pop("request_id", None)
            response_callback = request.context.get('response_callback') or \
                request.context.options.pop('response_hook', self._response_callback)

            response = await self.next.send(request)
            if metadata is None and request_id is None:
                data = json.loads(response.http_response.internal_response.text)
                request_id = data['requestId']
                metadata = data['metadata']
            for pipeline_obj in [request, response]:
                pipeline_obj.metadata = metadata
                pipeline_obj.request_id = request_id
            if response_callback:
                if asyncio.iscoroutine(response_callback):
                    await response_callback(response)
                else:
                    response_callback(response)
                request.context.response_callback = response_callback
            return response
        return await self.next.send(request)


