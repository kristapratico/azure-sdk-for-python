# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, Union, IO, Any, overload, Optional
from azure.core.polling import AsyncLROPoller
from azure.core.tracing.decorator_async import distributed_trace_async
from ._client import ConversationAnalysisClient as GeneratedConversationAnalysisClient
from .._projects._operations._operations import JSON
from .._projects.aio import ConversationAnalysisProjectsClient as GeneratedConversationAnalysisProjectsClient


class ConversationAnalysisClient(GeneratedConversationAnalysisClient):
    @overload
    async def analyze_conversation(self, task: JSON, *, content_type: str = "application/json", **kwargs: Any) -> JSON:
        ...

    @overload
    async def analyze_conversation(self, task: IO, *, content_type: str = "application/json", **kwargs: Any) -> JSON:
        ...

    @distributed_trace_async
    async def analyze_conversation(self, task: Union[JSON, IO], **kwargs: Any) -> JSON:
        return await super().analyze_conversation(task, **kwargs)



class ConversationAnalysisProjectsClient(GeneratedConversationAnalysisProjectsClient):
    
    @overload
    async def create_project(
        self, project_name: str, body: JSON, *, content_type: str = "application/merge-patch+json", **kwargs: Any
    ) -> JSON:
        ...

    @overload
    async def create_project(
        self, project_name: str, body: IO, *, content_type: str = "application/merge-patch+json", **kwargs: Any
    ) -> JSON:
        ...

    @distributed_trace_async
    async def create_project(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> JSON:
        return await super().create_project(project_name, body, **kwargs)

    @overload
    async def begin_import_project(
        self,
        project_name: str,
        body: JSON,
        *,
        exported_project_format: Optional[str] = None,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @overload
    async def begin_import_project(
        self,
        project_name: str,
        body: IO,
        *,
        exported_project_format: Optional[str] = None,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @distributed_trace_async
    async def begin_import_project(
        self, project_name: str, body: Union[JSON, IO], *, exported_project_format: Optional[str] = None, **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        return await super().begin_import_project(project_name, body, exported_project_format=exported_project_format, **kwargs)

    @overload
    async def begin_train(
        self, project_name: str, body: JSON, *, content_type: str = "application/json", **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @overload
    async def begin_train(
        self, project_name: str, body: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @distributed_trace_async
    async def begin_train(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> AsyncLROPoller[JSON]:
        return super().begin_train(project_name, body, **kwargs)

    @overload
    async def begin_swap_deployments(
        self, project_name: str, body: JSON, *, content_type: str = "application/json", **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @overload
    async def begin_swap_deployments(
        self, project_name: str, body: IO, *, content_type: str = "application/json", **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @distributed_trace_async
    async def begin_swap_deployments(self, project_name: str, body: Union[JSON, IO], **kwargs: Any) -> AsyncLROPoller[JSON]:
        return await super().begin_swap_deployments(project_name, body, **kwargs)

    @overload
    async def begin_deploy_project(
        self,
        project_name: str,
        deployment_name: str,
        body: JSON,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @overload
    async def begin_deploy_project(
        self,
        project_name: str,
        deployment_name: str,
        body: IO,
        *,
        content_type: str = "application/json",
        **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        ...

    @distributed_trace_async
    async def begin_deploy_project(
        self, project_name: str, deployment_name: str, body: Union[JSON, IO], **kwargs: Any
    ) -> AsyncLROPoller[JSON]:
        return await super().begin_deploy_project(project_name, deployment_name, body, **kwargs)



__all__: List[str] = [
    "ConversationAnalysisProjectsClient", "ConversationAnalysisClient"
]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
