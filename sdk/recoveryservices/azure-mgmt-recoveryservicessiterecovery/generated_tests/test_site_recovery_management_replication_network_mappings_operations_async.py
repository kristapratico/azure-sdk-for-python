# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.recoveryservicessiterecovery.aio import SiteRecoveryManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer
from devtools_testutils.aio import recorded_by_proxy_async

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestSiteRecoveryManagementReplicationNetworkMappingsOperationsAsync(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(SiteRecoveryManagementClient, is_async=True)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_list_by_replication_networks(self, resource_group):
        response = self.client.replication_network_mappings.list_by_replication_networks(
            fabric_name="str",
            network_name="str",
            api_version="2025-01-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_get(self, resource_group):
        response = await self.client.replication_network_mappings.get(
            fabric_name="str",
            network_name="str",
            network_mapping_name="str",
            api_version="2025-01-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_begin_create(self, resource_group):
        response = await (
            await self.client.replication_network_mappings.begin_create(
                fabric_name="str",
                network_name="str",
                network_mapping_name="str",
                input={
                    "properties": {
                        "recoveryNetworkId": "str",
                        "fabricSpecificDetails": "fabric_specific_create_network_mapping_input",
                        "recoveryFabricName": "str",
                    }
                },
                api_version="2025-01-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_begin_delete(self, resource_group):
        response = await (
            await self.client.replication_network_mappings.begin_delete(
                fabric_name="str",
                network_name="str",
                network_mapping_name="str",
                api_version="2025-01-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_begin_update(self, resource_group):
        response = await (
            await self.client.replication_network_mappings.begin_update(
                fabric_name="str",
                network_name="str",
                network_mapping_name="str",
                input={
                    "properties": {
                        "fabricSpecificDetails": "fabric_specific_update_network_mapping_input",
                        "recoveryFabricName": "str",
                        "recoveryNetworkId": "str",
                    }
                },
                api_version="2025-01-01",
            )
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy_async
    async def test_replication_network_mappings_list(self, resource_group):
        response = self.client.replication_network_mappings.list(
            api_version="2025-01-01",
        )
        result = [r async for r in response]
        # please add some check logic here by yourself
        # ...
