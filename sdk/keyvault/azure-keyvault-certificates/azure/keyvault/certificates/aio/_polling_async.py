# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
from typing import Any, Callable, cast, Optional, Union

from azure.core.pipeline import PipelineResponse
from azure.core.pipeline.transport import AsyncHttpTransport
from azure.core.polling import AsyncPollingMethod

from .._models import KeyVaultCertificate, CertificateOperation


class CreateCertificatePollerAsync(AsyncPollingMethod):
    def __init__(
        self, pipeline_response: PipelineResponse, get_certificate_command: Callable, interval: int = 5
    ) -> None:
        self._pipeline_response = pipeline_response
        self._command: Optional[Callable] = None
        self._resource: Optional[Union[CertificateOperation, KeyVaultCertificate]] = None
        self._pending_certificate_op: Optional[CertificateOperation] = None
        self._get_certificate_command = get_certificate_command
        self._polling_interval = interval

    async def _update_status(self) -> None:
        self._pending_certificate_op = await self._command() if self._command else None

    def initialize(self, client: Any, initial_response: Any, _: Callable) -> None:
        self._command = client
        self._pending_certificate_op = initial_response

    async def run(self) -> None:
        while not self.finished():
            await self._update_status()
            if not self.finished():
                # We should always ask the client's transport to sleep, instead of sleeping directly
                transport: AsyncHttpTransport = cast(AsyncHttpTransport, self._pipeline_response.context.transport)
                await transport.sleep(self._polling_interval)
        operation = self._pending_certificate_op
        if operation and operation.status and operation.status.lower() == "completed":
            self._resource = await self._get_certificate_command()
        else:
            self._resource = self._pending_certificate_op

    def finished(self) -> bool:
        operation = self._pending_certificate_op
        if operation and operation.issuer_name and operation.issuer_name.lower() == "unknown":
            # Because we've finished, self._resource won't be set by the run method; set it here so we don't return None
            self._resource = self._pending_certificate_op
            return True
        return self._pending_certificate_op.status.lower() != "inprogress"  # type: ignore

    def resource(self) -> Union[KeyVaultCertificate, CertificateOperation]:
        return self._resource  # type: ignore

    def status(self) -> str:
        return self._pending_certificate_op.status.lower()  # type: ignore
