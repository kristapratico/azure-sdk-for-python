# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, overload, Union, IO, Any, Optional
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace
from ._client import ConversationAnalysisProjectsClient as GeneratedConversationAnalysisProjectsClient
from ._operations._operations import JSON


class ConversationAnalysisProjectsClient(GeneratedConversationAnalysisProjectsClient):
    @overload
    def create_project(
        self, project_name: str, body: JSON, *, content_type: str = "application/merge-patch+json", **kwargs: Any
    ) -> JSON:
        ...

    @overload
    def create_project(
        self, project_name: str, body: IO, *, content_type: str = "application/merge-patch+json", **kwargs: Any
    ) -> JSON:
        ...

    @distributed_trace
    def create_project(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> JSON:
        return super().create_project(project_name, body, **kwargs)

    @overload
    def begin_import_project(
        self,
        project_name: str,
        body: JSON,
        *,
        exported_project_format: Optional[str] = None,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @overload
    def begin_import_project(
        self,
        project_name: str,
        body: IO,
        *,
        exported_project_format: Optional[str] = None,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @distributed_trace
    def begin_import_project(
        self, project_name: str, body: Union[JSON, IO], *, exported_project_format: Optional[str] = None, **kwargs: Any
    ) -> LROPoller[JSON]:
        return super().begin_import_project(
            project_name, body, exported_project_format=exported_project_format, **kwargs
        )

    @overload
    def begin_train(
        self, project_name: str, body: JSON, *, content_type: str = "application/json", **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @overload
    def begin_train(
        self, project_name: str, body: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @distributed_trace
    def begin_train(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> LROPoller[JSON]:
        return super().begin_train(project_name, body, **kwargs)

    @overload
    def begin_swap_deployments(
        self, project_name: str, body: JSON, *, content_type: str = "application/json", **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @overload
    def begin_swap_deployments(
        self, project_name: str, body: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @distributed_trace
    def begin_swap_deployments(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> LROPoller[JSON]:
        return super().begin_swap_deployments(project_name, body, **kwargs)

    @overload
    def begin_deploy_project(
        self,
        project_name: str,
        deployment_name: str,
        body: JSON,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @overload
    def begin_deploy_project(
        self,
        project_name: str,
        deployment_name: str,
        body: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> LROPoller[JSON]:
        ...

    @distributed_trace
    def begin_deploy_project(
        self, project_name: str, deployment_name: str, body: Union[JSON, IO], **kwargs: Any
    ) -> LROPoller[JSON]:
        return super().begin_deploy_project(project_name, deployment_name, body, **kwargs)


__all__: List[str] = [
    "ConversationAnalysisProjectsClient",
]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
