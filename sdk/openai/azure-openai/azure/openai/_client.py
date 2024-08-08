# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from openai import AzureOpenAI as SyncClient, Stream
from openai.resources.chat import Chat as OpenAIChat, Completions as OpenAICompletions
from openai.resources.beta import Beta as OpenAIBeta
from openai.resources.beta.assistants import Assistants as OpenAIAssistants
from azure.openai.types.chat._content_filtering import AzureChatCompletionChunk


class Completions(OpenAICompletions):
    def __getattribute__(self, name):
        if name == "create":

            def create_wrapper(*args, **kwargs):
                # modify request body for any azure-only options
                if "data_sources" in kwargs:
                    kwargs.setdefault("extra_body", {})
                    kwargs["extra_body"].update({"data_sources": kwargs.pop("data_sources")})

                result = super(Completions, self).__getattribute__("create")(*args, **kwargs)
                # transform response for any azure-only options?
                if "stream" in kwargs and kwargs["stream"] is True:
                    return Stream(cast_to=AzureChatCompletionChunk, response=result.response, client=result._client)
                return result
            return create_wrapper
        return super().__getattribute__(name)


class Chat(OpenAIChat):
    def __getattribute__(self, name):
        if name == "completions":
            return Completions(self._client)
        return super().__getattribute__(name)


class Assistants(OpenAIAssistants):
    def __getattribute__(self, name):
        if name == "create":

            def create_wrapper(*args, **kwargs):
                # modify request body for any azure-only options

                result = super(Assistants, self).__getattribute__("create")(*args, **kwargs)
                # transform response for any azure-only options?

                return result
            return create_wrapper
        return super().__getattribute__(name)


class Beta(OpenAIBeta):
    def __getattribute__(self, name):
        if name == "assistants":
            return Assistants(self._client)
        return super().__getattribute__(name)


class AzureOpenAI(SyncClient):
    chat: Chat
    def __getattribute__(self, name):
        if name == "chat":
            return Chat(self)
        if name == "beta":
            return Beta(self)
        return super().__getattribute__(name)
