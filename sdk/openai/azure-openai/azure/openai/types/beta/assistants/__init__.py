from __future__ import annotations

from typing import Union
from typing_extensions import TypedDict, Literal, TypeAlias

from openai import BaseModel
from openai.types.beta.assistant import Assistant, AssistantTool
from openai.types.beta.assistant_tool_param import AssistantToolParam
from openai.types.beta.threads.text import Text
from openai.types.beta.threads.annotation import Annotation
from openai.types.beta.threads.runs import ToolCall

__all__ = [
    "CustomToolParam",
    "CustomTool",
    "AzureAssistantTool",
    "AzureAssistant",
    "AzureAssistantToolParam",
    "AzureToolCall",
    "AzureText",
    "URLCitation",
    "Citation",
]

# TODO don't derive from openai types

class Citation(BaseModel):
    title: str
    url: str

class URLCitation(BaseModel):
    type: Literal["url_citation"]
    url_citation: Citation
    text: str


class AzureText(Text):
    annotations: list[AzureAnnotation]


class CustomToolParam(TypedDict, total=False):
    type: Literal["custom"]
    custom: object


class CustomTool(BaseModel):
    type: Literal["custom"]
    custom: object

class AzureAssistant(Assistant):
    tools: list[AzureAssistantTool]


class CustomToolCall(BaseModel):
    type: Literal["custom"]
    id: str
    index: int


AzureToolCall = Union[ToolCall, CustomToolCall]
AzureAnnotation: TypeAlias = Union[Annotation, URLCitation]
AzureAssistantTool: TypeAlias = Union[AssistantTool, CustomTool]
AzureAssistantToolParam: TypeAlias = Union[AssistantToolParam, CustomToolParam]
