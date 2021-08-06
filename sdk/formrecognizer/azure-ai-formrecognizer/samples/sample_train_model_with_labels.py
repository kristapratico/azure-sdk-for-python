# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_train_model_with_labels.py

DESCRIPTION:
    This sample demonstrates how to train a model with labels. For this sample, you can use the training
    forms found in https://aka.ms/azsdk/formrecognizer/sampletrainingfiles

    Upload the forms to your storage container and then generate a container SAS URL using these instructions:
    https://docs.microsoft.com/azure/cognitive-services/form-recognizer/quickstarts/get-started-with-form-recognizer#train--analyze-a-custom-form
    More details on setting up a container and required file structure can be found here:
    https://docs.microsoft.com/azure/cognitive-services/form-recognizer/build-training-data-set

    To see how to label your documents, you can use the service's labeling tool to label your documents:
    https://docs.microsoft.com/azure/cognitive-services/form-recognizer/label-tool?tabs=v2-1. Follow the
    instructions to store these labeled files in your blob container with the other form files.
    See sample_recognize_custom_forms.py to recognize forms with your custom model.

USAGE:
    python sample_train_model_with_labels.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_FORM_RECOGNIZER_ENDPOINT - the endpoint to your Cognitive Services resource.
    2) AZURE_FORM_RECOGNIZER_KEY - your Form Recognizer API key
    3) CONTAINER_SAS_URL - The shared access signature (SAS) Url of your Azure Blob Storage container with your labeled data.
        See https://docs.microsoft.com/azure/cognitive-services/form-recognizer/quickstarts/get-started-with-form-recognizer#train--analyze-a-custom-form
        for more detailed descriptions on how to get it.
"""

import os


class TrainModelWithLabelsSample(object):

    def train_model_with_labels(self):
        from azure.ai.formrecognizer import FormTrainingClient
        from azure.core.credentials import AzureKeyCredential

        endpoint = os.environ["AZURE_FORM_RECOGNIZER_ENDPOINT"]
        key = os.environ["AZURE_FORM_RECOGNIZER_KEY"]
        container_sas_url = os.environ["CONTAINER_SAS_URL"]

        form_training_client = FormTrainingClient(endpoint, AzureKeyCredential(key))
        poller = form_training_client.begin_build_model(
            source=container_sas_url, technique="fixedTemplate-2021-07-30"  # we set model_id internally
        )
        model = poller.result()

        # Custom model information
        print("Model ID: {}".format(model.model_id))

        print("Recognized doc types:")
        for doc_type, fields in model.doc_types.items():
            print("Doc type {} can recognize fields:".format(doc_type))
            for name, field in fields.field_schema.items():
                print("Name: {}, type: {}".format(name, field.type))
            for name, confidence in fields.field_confidence.items():
                print("Name: {}, confidence: {}".format(name, confidence))


if __name__ == '__main__':
    sample = TrainModelWithLabelsSample()
    sample.train_model_with_labels()
