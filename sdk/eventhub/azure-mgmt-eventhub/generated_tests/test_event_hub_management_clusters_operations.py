# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.eventhub import EventHubManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestEventHubManagementClustersOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(EventHubManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_list_available_cluster_region(self, resource_group):
        response = self.client.clusters.list_available_cluster_region(
            api_version="2018-01-01-preview",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_list_by_resource_group(self, resource_group):
        response = self.client.clusters.list_by_resource_group(
            resource_group_name=resource_group.name,
            api_version="2018-01-01-preview",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_get(self, resource_group):
        response = self.client.clusters.get(
            resource_group_name=resource_group.name,
            cluster_name="str",
            api_version="2018-01-01-preview",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_begin_create_or_update(self, resource_group):
        response = self.client.clusters.begin_create_or_update(
            resource_group_name=resource_group.name,
            cluster_name="str",
            parameters={
                "createdAt": "str",
                "id": "str",
                "location": "str",
                "metricId": "str",
                "name": "str",
                "sku": {"name": "str", "capacity": 0},
                "status": "str",
                "tags": {"str": "str"},
                "type": "str",
                "updatedAt": "str",
            },
            api_version="2018-01-01-preview",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_begin_update(self, resource_group):
        response = self.client.clusters.begin_update(
            resource_group_name=resource_group.name,
            cluster_name="str",
            parameters={
                "createdAt": "str",
                "id": "str",
                "location": "str",
                "metricId": "str",
                "name": "str",
                "sku": {"name": "str", "capacity": 0},
                "status": "str",
                "tags": {"str": "str"},
                "type": "str",
                "updatedAt": "str",
            },
            api_version="2018-01-01-preview",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_begin_delete(self, resource_group):
        response = self.client.clusters.begin_delete(
            resource_group_name=resource_group.name,
            cluster_name="str",
            api_version="2018-01-01-preview",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_list_namespaces(self, resource_group):
        response = self.client.clusters.list_namespaces(
            resource_group_name=resource_group.name,
            cluster_name="str",
            api_version="2018-01-01-preview",
        )

        # please add some check logic here by yourself
        # ...
