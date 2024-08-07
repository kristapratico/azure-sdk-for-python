# coding: utf-8
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -------------------------------------------------------------------------
import pytest
import json
from testcase import WebpubsubTest, WebpubsubPowerShellPreparer
from azure.messaging.webpubsubservice._operations._operations import build_web_pub_sub_service_send_to_all_request
from azure.core.exceptions import ServiceRequestError, HttpResponseError
from devtools_testutils import recorded_by_proxy

@pytest.mark.live_test_only
class TestWebpubsubSmoke(WebpubsubTest):


    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_webpubsub_send_to_all(self, webpubsub_endpoint):
        client = self.create_client(endpoint=webpubsub_endpoint, hub='hub')
        client.send_to_all({'hello': 'test_webpubsub_send_to_all'})

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_webpubsub_send_to_all_api_management_proxy(self, webpubsub_endpoint, webpubsub_reverse_proxy_endpoint=None):
        client = self.create_client(endpoint=webpubsub_endpoint, hub='hub', reverse_proxy_endpoint=webpubsub_reverse_proxy_endpoint)
        client.send_to_all({'hello': 'test_webpubsub_send_to_all_api_management_proxy'})

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_webpubsub_send_request(self, webpubsub_endpoint):
        client = self.create_client(endpoint=webpubsub_endpoint, hub='hub')
        request = build_web_pub_sub_service_send_to_all_request('Hub', content='test_webpubsub_send_request', content_type='text/plain')
        response = client.send_request(request)
        assert response.status_code == 202

    # If reverse_proxy_endpoint is not available, `ServiceRequestError` will be raised
    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_webpubsub_send_to_all_api_management_proxy_counter_test(self, webpubsub_endpoint):
        client = self.create_client(endpoint=webpubsub_endpoint, hub='hub', reverse_proxy_endpoint='https://example.azure-api.net')
        with pytest.raises((ServiceRequestError, HttpResponseError)) as exc_info:
            client.send_to_all({'hello': 'test_webpubsub_send_to_all_api_management_proxy_counter_test'})
            
        # Make sure the HttpResponseError is raised for the same reason: DNS lookup failure
        if exc_info.type is HttpResponseError:
            response_content = json.loads(exc_info.value.response.content)
            assert "No such host is known" in response_content["Message"] or "Name or service not known" in response_content["Message"] # The former for Windows and the latter for Linux

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_get_client_access_token(self, webpubsub_endpoint):
        client = self.create_client(endpoint=webpubsub_endpoint, hub='hub')
        access_token = client.get_client_access_token()
        assert len(access_token) == 3
        assert access_token['baseUrl'][:3] == "wss"
        assert access_token['token']
        assert access_token['url'][:3] == "wss"

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_hello_world_with_connection_string(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.send_to_all(message="Hello, World!", content_type="text/plain")

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_hello_world_with_connection_string_json(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.send_to_all(message={"hello": "world!"})

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_hello_world_with_connection_string_binary(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.send_to_all(message=b"Hello, World!", content_type="application/octet-stream")

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_no_users_groups(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        assert not client.user_exists(user_id="fake user")
        assert not client.group_exists(group="fake group")

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_remove_connection_from_all_groups(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.remove_connection_from_all_groups(connection_id="fake connection id")

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_send_with_filter(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.send_to_all(message={"hello": "world!"}, filter="userId ne 'user1'", content_type="text/plain")

    @WebpubsubPowerShellPreparer()
    @recorded_by_proxy
    def test_get_client_access_key_with_groups(self, webpubsub_connection_string):
        client = self.create_client(connection_string=webpubsub_connection_string, hub="hub")
        client.get_client_access_token(user_id="user1", groups=["groups1"])