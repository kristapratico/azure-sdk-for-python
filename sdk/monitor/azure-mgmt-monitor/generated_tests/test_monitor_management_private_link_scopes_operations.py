# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.monitor import MonitorManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestMonitorManagementPrivateLinkScopesOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(MonitorManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_list(self, resource_group):
        response = self.client.private_link_scopes.list(
            api_version="2019-10-17-preview",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_list_by_resource_group(self, resource_group):
        response = self.client.private_link_scopes.list_by_resource_group(
            resource_group_name=resource_group.name,
            api_version="2019-10-17-preview",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_begin_delete(self, resource_group):
        response = self.client.private_link_scopes.begin_delete(
            resource_group_name=resource_group.name,
            scope_name="str",
            api_version="2019-10-17-preview",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_get(self, resource_group):
        response = self.client.private_link_scopes.get(
            resource_group_name=resource_group.name,
            scope_name="str",
            api_version="2019-10-17-preview",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_create_or_update(self, resource_group):
        response = self.client.private_link_scopes.create_or_update(
            resource_group_name=resource_group.name,
            scope_name="str",
            azure_monitor_private_link_scope_payload={
                "location": "str",
                "id": "str",
                "name": "str",
                "privateEndpointConnections": [
                    {
                        "id": "str",
                        "name": "str",
                        "privateEndpoint": {"id": "str"},
                        "privateLinkServiceConnectionState": {
                            "description": "str",
                            "status": "str",
                            "actionsRequired": "str",
                        },
                        "provisioningState": "str",
                        "type": "str",
                    }
                ],
                "provisioningState": "str",
                "tags": {"str": "str"},
                "type": "str",
            },
            api_version="2019-10-17-preview",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_private_link_scopes_update_tags(self, resource_group):
        response = self.client.private_link_scopes.update_tags(
            resource_group_name=resource_group.name,
            scope_name="str",
            private_link_scope_tags={"tags": {"str": "str"}},
            api_version="2019-10-17-preview",
        )

        # please add some check logic here by yourself
        # ...
