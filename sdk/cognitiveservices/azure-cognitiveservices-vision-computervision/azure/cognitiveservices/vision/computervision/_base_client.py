from azure.cognitiveservices.vision.computervision._policies import CognitiveServicesCredentialPolicy
from azure.core import Configuration
from azure.core.pipeline import Pipeline
from azure.core.pipeline import policies
from azure.core.pipeline.transport import RequestsTransport
from azure.core.pipeline.policies.distributed_tracing import DistributedTracingPolicy
from .version import VERSION


class ComputerVisionClientBase(object):

    def __init__(self, endpoint, credentials, **kwargs):
        self._config, self._pipeline = self._create_pipeline(credentials, **kwargs)
        self._config.generate_client_request_id = True
        self._config.endpoint = endpoint

    def _create_pipeline(self, credentials, **kwargs):
        self.credential_policy = CognitiveServicesCredentialPolicy(credentials, **kwargs)

        config = self.create_configuration(**kwargs)
        config.transport = kwargs.get("transport")  # type: ignore
        if not config.transport:
            config.transport = RequestsTransport(**kwargs)
        config.user_agent_policy.add_user_agent('azsdk-python-computervisionclient/{}'.format(VERSION))

        policies = [
            config.user_agent_policy,
            config.headers_policy,
            self.credential_policy,
            config.proxy_policy,
            config.logging_policy,
            config.retry_policy,
            config.custom_hook_policy,
            config.redirect_policy,
            DistributedTracingPolicy()
        ]
        return config, Pipeline(config.transport, policies=policies)

    def create_configuration(self, **kwargs):
        config = Configuration(**kwargs)
        config.user_agent_policy = kwargs.get('user_agent_policy') or policies.UserAgentPolicy(**kwargs)
        config.headers_policy = kwargs.get('headers_policy') or policies.HeadersPolicy(**kwargs)
        config.proxy_policy = kwargs.get('proxy_policy') or policies.ProxyPolicy(**kwargs)
        config.logging_policy = kwargs.get('logging_policy') or policies.NetworkTraceLoggingPolicy(**kwargs)
        config.retry_policy = kwargs.get('retry_policy') or policies.RetryPolicy(**kwargs)
        config.custom_hook_policy = kwargs.get('custom_hook_policy') or policies.CustomHookPolicy(**kwargs)
        config.redirect_policy = kwargs.get('redirect_policy') or policies.RedirectPolicy(**kwargs)

        return config
