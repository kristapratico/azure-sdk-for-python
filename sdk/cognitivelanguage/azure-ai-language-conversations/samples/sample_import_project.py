# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

"""
FILE: sample_import_project.py

DESCRIPTION:
    This sample demonstrates how to import a project.

USAGE:
    python sample_import_project.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_CONVERSATIONS_ENDPOINT                       - endpoint for your CLU resource.
    2) AZURE_CONVERSATIONS_KEY                            - API key for your CLU resource.
    3) AZURE_CONVERSATIONS_WORKFLOW_PROJECT_NAME     - project name for your CLU orchestration project.
    4) AZURE_CONVERSATIONS_WORKFLOW_DEPLOYMENT_NAME  - deployment name for your CLU orchestration project.
"""

def sample_import_project():
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisProjectsClient

    clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
    project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]

    exported_project_assets = {
        "projectKind": "Conversation",
        "intents": [
        {
            "category": "Read"
        },
        {
            "category": "Delete"
        }
        ],
        "entities": [
        {
            "category": "Sender"
        }
        ],
        "utterances": [
        {
            "text": "Open Blake's email",
            "dataset": "Train",
            "intent": "Read",
            "entities": [
            {
                "category": "Sender",
                "offset": 5,
                "length": 5
            }
            ]
        },
        {
            "text": "Delete last email",
            "language": "en-gb",
            "dataset": "Test",
            "intent": "Delete",
            "entities": []
        }
        ]
    }

    client = ConversationAnalysisProjectsClient(clu_endpoint, AzureKeyCredential(clu_key))
    poller = client.begin_import_project(
        project_name=project_name,
        body={
            "assets": exported_project_assets,
            "metadata": {
                "projectKind": "Conversation",
                "settings": {
                "confidenceThreshold": 0.7
                },
                "projectName": "EmailApp",
                "multilingual": True,
                "description": "Trying out CLU",
                "language": "en-us"
            },
            "projectFileVersion": "2022-05-01"
        }
    )
    response = poller.result()
    print(response)


def sample_train_model():
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisProjectsClient

    clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
    project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]

    client = ConversationAnalysisProjectsClient(clu_endpoint, AzureKeyCredential(clu_key))

    poller = client.begin_train(
        project_name=project_name,
        body={
            "modelLabel": "sample",
            "trainingMode": "standard"
        }
    )

    response = poller.result()
    print(response)


def sample_deploy_model():
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.language.conversations import ConversationAnalysisProjectsClient

    clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
    clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
    project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
    deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]

    client = ConversationAnalysisProjectsClient(clu_endpoint, AzureKeyCredential(clu_key))

    poller = client.begin_deploy_project(
        project_name=project_name,
        deployment_name=deployment_name,
        body={
            "trainedModelLabel": "sample"
        }
    )
    response = poller.result()
    print(response)


if __name__ == '__main__':
    sample_import_project()
    sample_train_model()
    sample_deploy_model()
