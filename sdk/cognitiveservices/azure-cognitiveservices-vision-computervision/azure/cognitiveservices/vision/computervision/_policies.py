from azure.core.pipeline.policies import SansIOHTTPPolicy, HTTPPolicy
import json

class CognitiveServicesCredentialPolicy(SansIOHTTPPolicy):

    def __init__(self, cognitiveservices_key, **kwargs):
        self.cognitiveservices_key = cognitiveservices_key
        super(CognitiveServicesCredentialPolicy, self).__init__()

    def on_request(self, request):
        request.http_request.headers["Ocp-Apim-Subscription-Key"] = self.cognitiveservices_key
        request.http_request.headers["X-BingApis-SDK-Client"] = "Python-SDK"


class ComputerVisionResponseHook(HTTPPolicy):

    def __init__(self, **kwargs):  # pylint: disable=unused-argument
        self._response_callback = kwargs.get('raw_response_hook')
        super(ComputerVisionResponseHook, self).__init__()

    def send(self, request):
        if self._response_callback:
            metadata = request.context.get("metadata") or \
                request.context.options.pop("metadata", None)
            request_id = request.context.get("request_id") or \
                request.context.options.pop("request_id", None)
            response_callback = request.context.get('response_callback') or \
                request.context.options.pop('raw_response_hook', self._response_callback)

            response = self.next.send(request)
            if metadata is None and request_id is None:
                data = response.http_response.internal_response.text.split('"requestId":')[1]
                request_id, metadata = data.split('","metadata":')
                metadata = json.loads(metadata[0:-1])
                request_id = request_id[1:]
            for pipeline_obj in [request, response]:
                pipeline_obj.context['metadata'] = metadata
                pipeline_obj.context['request_id'] = request_id
            if response_callback:
                response_callback(response)
                request.context['response_callback'] = response_callback
            return response
        return self.next.send(request)

