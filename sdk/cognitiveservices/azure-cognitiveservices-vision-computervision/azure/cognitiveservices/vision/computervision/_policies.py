from azure.core.pipeline.policies import SansIOHTTPPolicy
from msrest.authentication import CognitiveServicesCredentials

class CognitiveServicesCredentialPolicy(SansIOHTTPPolicy):

    def __init__(self, cognitiveservices_key, **kwargs):
        if isinstance(cognitiveservices_key, CognitiveServicesCredentials):
            cognitiveservices_key = cognitiveservices_key.in_headers["Ocp-Apim-Subscription-Key"]
        self.cognitiveservices_key = cognitiveservices_key
        super(CognitiveServicesCredentialPolicy, self).__init__()

    def on_request(self, request):
        request.http_request.headers["Ocp-Apim-Subscription-Key"] = self.cognitiveservices_key
        request.http_request.headers["X-BingApis-SDK-Client"] = "Python-SDK"
