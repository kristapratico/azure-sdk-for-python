# coding: utf-8

#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from azure.mgmt.informaticadatamanagement import InformaticaDataMgmtClient
from devtools_testutils import AzureMgmtRecordedTestCase, RandomNameResourceGroupPreparer, recorded_by_proxy

AZURE_LOCATION = 'eastus'

class TestMgmtInformaticaDataMgmt(AzureMgmtRecordedTestCase):

    def setup_method(self, method):
        self.client = self.create_mgmt_client(InformaticaDataMgmtClient)

    @RandomNameResourceGroupPreparer(location=AZURE_LOCATION)
    @recorded_by_proxy
    def test_list_organizations_by_resource_group(self, resource_group):
        assert list(self.client.organizations.list_by_resource_group(resource_group.name)) == []

    @recorded_by_proxy
    def test_list_operations(self):
        assert list(self.client.operations.list())
