# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) Python Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------
import pytest
from azure.mgmt.servicefabricmanagedclusters import ServiceFabricManagedClustersManagementClient

from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = "eastus"


@pytest.mark.skip("you may need to update the auto-generated test case before run it")
class TestServiceFabricManagedClustersManagementNodeTypesOperations(AzureMgmtRecordedTestCase):
    def setup_method(self, method):
        self.client = self.create_mgmt_client(ServiceFabricManagedClustersManagementClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_get(self, resource_group):
        response = self.client.node_types.get(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_create_or_update(self, resource_group):
        response = self.client.node_types.begin_create_or_update(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={
                "id": "str",
                "name": "str",
                "properties": {
                    "isPrimary": bool,
                    "vmInstanceCount": 0,
                    "additionalDataDisks": [{"diskLetter": "str", "diskSizeGB": 0, "diskType": "str", "lun": 0}],
                    "additionalNetworkInterfaceConfigurations": [
                        {
                            "ipConfigurations": [
                                {
                                    "name": "str",
                                    "applicationGatewayBackendAddressPools": [{"id": "str"}],
                                    "loadBalancerBackendAddressPools": [{"id": "str"}],
                                    "loadBalancerInboundNatPools": [{"id": "str"}],
                                    "privateIPAddressVersion": "str",
                                    "publicIPAddressConfiguration": {
                                        "name": "str",
                                        "ipTags": [{"ipTagType": "str", "tag": "str"}],
                                        "publicIPAddressVersion": "str",
                                    },
                                    "subnet": {"id": "str"},
                                }
                            ],
                            "name": "str",
                            "dscpConfiguration": {"id": "str"},
                            "enableAcceleratedNetworking": bool,
                        }
                    ],
                    "applicationPorts": {"endPort": 0, "startPort": 0},
                    "capacities": {"str": "str"},
                    "computerNamePrefix": "str",
                    "dataDiskLetter": "str",
                    "dataDiskSizeGB": 0,
                    "dataDiskType": "str",
                    "dscpConfigurationId": "str",
                    "enableAcceleratedNetworking": bool,
                    "enableEncryptionAtHost": bool,
                    "enableNodePublicIP": bool,
                    "enableNodePublicIPv6": bool,
                    "enableOverProvisioning": bool,
                    "ephemeralPorts": {"endPort": 0, "startPort": 0},
                    "evictionPolicy": "str",
                    "frontendConfigurations": [
                        {
                            "applicationGatewayBackendAddressPoolId": "str",
                            "ipAddressType": "str",
                            "loadBalancerBackendAddressPoolId": "str",
                            "loadBalancerInboundNatPoolId": "str",
                        }
                    ],
                    "hostGroupId": "str",
                    "isSpotVM": bool,
                    "isStateless": bool,
                    "multiplePlacementGroups": bool,
                    "natConfigurations": [{"backendPort": 0, "frontendPortRangeEnd": 0, "frontendPortRangeStart": 0}],
                    "natGatewayId": "str",
                    "networkSecurityRules": [
                        {
                            "access": "str",
                            "direction": "str",
                            "name": "str",
                            "priority": 0,
                            "protocol": "str",
                            "description": "str",
                            "destinationAddressPrefix": "str",
                            "destinationAddressPrefixes": ["str"],
                            "destinationPortRange": "str",
                            "destinationPortRanges": ["str"],
                            "sourceAddressPrefix": "str",
                            "sourceAddressPrefixes": ["str"],
                            "sourcePortRange": "str",
                            "sourcePortRanges": ["str"],
                        }
                    ],
                    "placementProperties": {"str": "str"},
                    "provisioningState": "str",
                    "secureBootEnabled": bool,
                    "securityEncryptionType": "str",
                    "securityType": "str",
                    "serviceArtifactReferenceId": "str",
                    "spotRestoreTimeout": "str",
                    "subnetId": "str",
                    "useDefaultPublicLoadBalancer": bool,
                    "useEphemeralOSDisk": bool,
                    "useTempDataDisk": bool,
                    "vmApplications": [
                        {
                            "packageReferenceId": "str",
                            "configurationReference": "str",
                            "enableAutomaticUpgrade": bool,
                            "order": 0,
                            "treatFailureAsDeploymentFailure": bool,
                            "vmGalleryTags": "str",
                        }
                    ],
                    "vmExtensions": [
                        {
                            "name": "str",
                            "properties": {
                                "publisher": "str",
                                "type": "str",
                                "typeHandlerVersion": "str",
                                "autoUpgradeMinorVersion": bool,
                                "enableAutomaticUpgrade": bool,
                                "forceUpdateTag": "str",
                                "protectedSettings": {},
                                "provisionAfterExtensions": ["str"],
                                "provisioningState": "str",
                                "settings": {},
                                "setupOrder": ["str"],
                            },
                        }
                    ],
                    "vmImageOffer": "str",
                    "vmImagePlan": {"name": "str", "product": "str", "promotionCode": "str", "publisher": "str"},
                    "vmImagePublisher": "str",
                    "vmImageResourceId": "str",
                    "vmImageSku": "str",
                    "vmImageVersion": "str",
                    "vmManagedIdentity": {"userAssignedIdentities": ["str"]},
                    "vmSecrets": [
                        {
                            "sourceVault": {"id": "str"},
                            "vaultCertificates": [{"certificateStore": "str", "certificateUrl": "str"}],
                        }
                    ],
                    "vmSetupActions": ["str"],
                    "vmSharedGalleryImageId": "str",
                    "vmSize": "str",
                    "zoneBalance": bool,
                    "zones": ["str"],
                },
                "sku": {"capacity": 0, "name": "str", "tier": "str"},
                "systemData": {
                    "createdAt": "2020-02-20 00:00:00",
                    "createdBy": "str",
                    "createdByType": "str",
                    "lastModifiedAt": "2020-02-20 00:00:00",
                    "lastModifiedBy": "str",
                    "lastModifiedByType": "str",
                },
                "tags": {"str": "str"},
                "type": "str",
            },
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_update(self, resource_group):
        response = self.client.node_types.begin_update(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"sku": {"capacity": 0, "name": "str", "tier": "str"}, "tags": {"str": "str"}},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_delete(self, resource_group):
        response = self.client.node_types.begin_delete(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_list_by_managed_clusters(self, resource_group):
        response = self.client.node_types.list_by_managed_clusters(
            resource_group_name=resource_group.name,
            cluster_name="str",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_deallocate(self, resource_group):
        response = self.client.node_types.begin_deallocate(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_delete_node(self, resource_group):
        response = self.client.node_types.begin_delete_node(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_redeploy(self, resource_group):
        response = self.client.node_types.begin_redeploy(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_reimage(self, resource_group):
        response = self.client.node_types.begin_reimage(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_restart(self, resource_group):
        response = self.client.node_types.begin_restart(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_start(self, resource_group):
        response = self.client.node_types.begin_start(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"force": bool, "nodes": ["str"], "updateType": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_start_fault_simulation(self, resource_group):
        response = self.client.node_types.begin_start_fault_simulation(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"parameters": "fault_simulation_content"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_begin_stop_fault_simulation(self, resource_group):
        response = self.client.node_types.begin_stop_fault_simulation(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"simulationId": "str"},
        ).result()  # call '.result()' to poll until service return final result

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_get_fault_simulation(self, resource_group):
        response = self.client.node_types.get_fault_simulation(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
            parameters={"simulationId": "str"},
        )

        # please add some check logic here by yourself
        # ...

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_node_types_list_fault_simulation(self, resource_group):
        response = self.client.node_types.list_fault_simulation(
            resource_group_name=resource_group.name,
            cluster_name="str",
            node_type_name="str",
        )
        result = [r for r in response]
        # please add some check logic here by yourself
        # ...
