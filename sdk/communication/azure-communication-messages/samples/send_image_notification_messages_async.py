# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: send_image_notification_messages_async.py

DESCRIPTION:
    This sample demonstrates sending an Whatsapp message with image from business phone number to a single user. The NotificationMessageClient is 
    authenticated using a connection string.

USAGE:
    python send_image_notification_messages_async.py

    Set the environment variable with your own value before running the sample:
    1) COMMUNICATION_SAMPLES_CONNECTION_STRING - the connection string in your ACS resource
    2) RECIPIENT_PHONE_NUMBER - a phone number with Whatsapp capabilities
    3) WHATSAPP_CHANNEL_ID - Channel created in Azure portal for Advanced Messaging.
"""

import asyncio
import os
import sys
from typing import cast

sys.path.append("..")


class SendWhatsAppMessageSampleAsync(object):

    def __init__(self) -> None:
        connection_string = os.getenv("COMMUNICATION_SAMPLES_CONNECTION_STRING")
        phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")
        channel_id = os.getenv("WHATSAPP_CHANNEL_ID")
        
        if not connection_string:
            raise ValueError("COMMUNICATION_SAMPLES_CONNECTION_STRING environment variable must be set")
        if not phone_number:
            raise ValueError("RECIPIENT_PHONE_NUMBER environment variable must be set")
        if not channel_id:
            raise ValueError("WHATSAPP_CHANNEL_ID environment variable must be set")
            
        self.connection_string = cast(str, connection_string)
        self.phone_number = cast(str, phone_number)
        self.channel_id = cast(str, channel_id)

    async def send_image_send_message_async(self):
        from azure.communication.messages.aio import NotificationMessagesClient
        from azure.communication.messages.models import ImageNotificationContent

        # client creation
        messaging_client = NotificationMessagesClient.from_connection_string(self.connection_string)

        image_options = ImageNotificationContent(
            channel_registration_id=self.channel_id,
            to=[self.phone_number],
            content="Hello World via Notification Messaging SDK.",
            media_uri="https://aka.ms/acsicon1",
        )

        # calling send() with whatsapp message details
        async with messaging_client:
            message_responses = await messaging_client.send(image_options)
            response = message_responses.receipts[0]
            print("Message with message id {} was successful sent to {}".format(response.message_id, response.to))


async def main():
    sample = SendWhatsAppMessageSampleAsync()
    await sample.send_image_send_message_async()


if __name__ == "__main__":
    asyncio.run(main())
