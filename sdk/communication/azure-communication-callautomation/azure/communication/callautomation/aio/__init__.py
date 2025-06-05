# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Async client library for Azure Communication Call Automation."""
from ._call_automation_client_async import CallAutomationClient
from ._call_connection_client_async import CallConnectionClient

__all__ = ["CallAutomationClient", "CallConnectionClient"]
