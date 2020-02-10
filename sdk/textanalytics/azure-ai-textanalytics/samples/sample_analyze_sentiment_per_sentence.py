# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_analyze_sentiment.py

DESCRIPTION:
    This sample demonstrates how to analyze sentiment in a batch of documents.
    An overall and per-sentence sentiment is returned.

USAGE:
    python sample_analyze_sentiment.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_TEXT_ANALYTICS_ENDPOINT - the endpoint to your cognitive services resource.
    2) AZURE_TEXT_ANALYTICS_KEY - your text analytics subscription key
"""

import os


class AnalyzeSentimentSample(object):

    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")

    def analyze_sentiment(self):
        from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential
        text_analytics_client = TextAnalyticsClient(endpoint=self.endpoint, credential=TextAnalyticsApiKeyCredential(self.key))
        documents = [
            "Api is consistent, clean. Documentation is at its worst, fine."
        ]

        result = text_analytics_client.analyze_sentiment(documents)

        for idx, doc in enumerate(result):
            print(documents[idx])
            print("Sentiment: {}\n".format(doc.sentiment))
            for idx, sentence in enumerate(doc.sentences):
                print("Sentence {} sentiment: {}".format(idx+1, sentence.sentiment))


if __name__ == '__main__':
    sample = AnalyzeSentimentSample()
    sample.analyze_sentiment()
