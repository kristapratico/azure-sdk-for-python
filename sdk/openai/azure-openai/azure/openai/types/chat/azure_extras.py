from __future__ import annotations

from typing_extensions import TypedDict
from .on_your_data import AzureChatExtensionConfiguration


class AzureChatExtras(TypedDict, total=False):
    data_sources: list[AzureChatExtensionConfiguration]
