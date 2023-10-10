# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, Sequence, Optional
from azure.core.tracing.decorator import distributed_trace
from ._operations import EmbeddingsOperations as GeneratedEmbeddingsOperations
from ..models._models import Embeddings, EmbeddingsOptions

class EmbeddingsOperations(GeneratedEmbeddingsOperations):

    @distributed_trace
    def create(
        self,
        deployment_id: str,
        input: Sequence[str],
        *,
        user: Optional[str] = None,
        **kwargs
    ) -> Embeddings:
        return super()._create(
            deployment_id=deployment_id,
            body=EmbeddingsOptions(
                input=input,
                user=user
            ),
            **kwargs
        )


__all__: List[str] = ["EmbeddingsOperations"]  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
