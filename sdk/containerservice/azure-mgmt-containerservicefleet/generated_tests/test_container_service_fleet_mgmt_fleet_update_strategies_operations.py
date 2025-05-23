# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.containerservicefleet import ContainerServiceFleetMgmtClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestContainerServiceFleetMgmtFleetUpdateStrategiesOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ContainerServiceFleetMgmtClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_fleet_update_strategies_list_by_fleet(self, resource_group):
        response = self.client.fleet_update_strategies.list_by_fleet(
            resource_group_name=resource_group.name,
            fleet_name="str",
            api_version="2025-03-01",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_fleet_update_strategies_get(self, resource_group):
        response = self.client.fleet_update_strategies.get(
            resource_group_name=resource_group.name,
            fleet_name="str",
            update_strategy_name="str",
            api_version="2025-03-01",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_fleet_update_strategies_begin_create_or_update(self, resource_group):
        response = self.client.fleet_update_strategies.begin_create_or_update(
            resource_group_name=resource_group.name,
            fleet_name="str",
            update_strategy_name="str",
            resource={
                "eTag": "str",
                "id": "str",
                "name": "str",
                "provisioningState": "str",
                "strategy": {"stages": [{"name": "str", "afterStageWaitInSeconds": 0, "groups": [{"name": "str"}]}]},
                "systemData": {
                    "createdAt": "2020-02-20 00:00:00",
                    "createdBy": "str",
                    "createdByType": "str",
                    "lastModifiedAt": "2020-02-20 00:00:00",
                    "lastModifiedBy": "str",
                    "lastModifiedByType": "str",
                },
                "type": "str",
            },
            api_version="2025-03-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_fleet_update_strategies_begin_delete(self, resource_group):
        response = self.client.fleet_update_strategies.begin_delete(
            resource_group_name=resource_group.name,
            fleet_name="str",
            update_strategy_name="str",
            api_version="2025-03-01",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...
