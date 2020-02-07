import os


# endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
# key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

def response_handler(response, _, response_headers):
    return response


def testing_receipt():
    from azure.core.polling import LROPoller
    from azure.cognitiveservices.formrecognizer import FormRecognizerClient
    from azure.cognitiveservices.formrecognizer.models import AnalyzeOperationResult, SourcePath
    from azure.mgmt.core.polling.arm_polling import ARMPolling


    client = FormRecognizerClient(endpoint=endpoint, credential=key)
    response = client.analyze_receipt_async(
        file_stream={"source": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"},
        include_text_details=True,
        cls=response_handler)

    if response.http_response.status_code != 202:
        print("analyze failed")
        exit()
    print("analyze succeeded")

    poll_method = ARMPolling()
    poller = LROPoller(client._client, response, AnalyzeOperationResult, poll_method)
    result = poller.result()
    print(result)
