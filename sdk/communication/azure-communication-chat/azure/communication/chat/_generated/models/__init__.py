# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._models_py3 import AddChatParticipantsRequest
from ._models_py3 import AddChatParticipantsResult
from ._models_py3 import ChatAttachment
from ._models_py3 import ChatError
from ._models_py3 import ChatMessage
from ._models_py3 import ChatMessageContent
from ._models_py3 import ChatMessageReadReceipt
from ._models_py3 import ChatMessageReadReceiptsCollection
from ._models_py3 import ChatMessagesCollection
from ._models_py3 import ChatParticipant
from ._models_py3 import ChatParticipantsCollection
from ._models_py3 import ChatThreadItem
from ._models_py3 import ChatThreadProperties
from ._models_py3 import ChatThreadsItemCollection
from ._models_py3 import CommunicationErrorResponse
from ._models_py3 import CommunicationIdentifierModel
from ._models_py3 import CommunicationUserIdentifierModel
from ._models_py3 import CreateChatThreadRequest
from ._models_py3 import CreateChatThreadResult
from ._models_py3 import MicrosoftTeamsAppIdentifierModel
from ._models_py3 import MicrosoftTeamsUserIdentifierModel
from ._models_py3 import PhoneNumberIdentifierModel
from ._models_py3 import SendChatMessageRequest
from ._models_py3 import SendChatMessageResult
from ._models_py3 import SendReadReceiptRequest
from ._models_py3 import SendTypingNotificationRequest
from ._models_py3 import UpdateChatMessageRequest
from ._models_py3 import UpdateChatThreadRequest

from ._azure_communication_chat_service_enums import ChatAttachmentType
from ._azure_communication_chat_service_enums import ChatMessageType
from ._azure_communication_chat_service_enums import CommunicationCloudEnvironmentModel
from ._azure_communication_chat_service_enums import CommunicationIdentifierModelKind
from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AddChatParticipantsRequest",
    "AddChatParticipantsResult",
    "ChatAttachment",
    "ChatError",
    "ChatMessage",
    "ChatMessageContent",
    "ChatMessageReadReceipt",
    "ChatMessageReadReceiptsCollection",
    "ChatMessagesCollection",
    "ChatParticipant",
    "ChatParticipantsCollection",
    "ChatThreadItem",
    "ChatThreadProperties",
    "ChatThreadsItemCollection",
    "CommunicationErrorResponse",
    "CommunicationIdentifierModel",
    "CommunicationUserIdentifierModel",
    "CreateChatThreadRequest",
    "CreateChatThreadResult",
    "MicrosoftTeamsAppIdentifierModel",
    "MicrosoftTeamsUserIdentifierModel",
    "PhoneNumberIdentifierModel",
    "SendChatMessageRequest",
    "SendChatMessageResult",
    "SendReadReceiptRequest",
    "SendTypingNotificationRequest",
    "UpdateChatMessageRequest",
    "UpdateChatThreadRequest",
    "ChatAttachmentType",
    "ChatMessageType",
    "CommunicationCloudEnvironmentModel",
    "CommunicationIdentifierModelKind",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
