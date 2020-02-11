import os


# endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
# key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def response_handler(response, _, response_headers):
    return response


def testing_receipt():
    from azure.core.polling import LROPoller
    from azure.cognitiveservices.formrecognizer import FormRecognizerClient
    from azure.cognitiveservices.formrecognizer.models import AnalyzeOperationResult
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

    for label, value in result.analyze_result.document_results[0].fields.items():
        print("{}: {}".format(label, value.value_string))


def testing_layout():
    from azure.core.polling import LROPoller
    from azure.cognitiveservices.formrecognizer import FormRecognizerClient
    from azure.cognitiveservices.formrecognizer.models import AnalyzeOperationResult
    from azure.mgmt.core.polling.arm_polling import ARMPolling

    client = FormRecognizerClient(endpoint=endpoint, credential=key)


    response = client.analyze_layout_async(
        file_stream={"source": "https://i.stack.imgur.com/1FyIg.png"},
        cls=response_handler)

    if response.http_response.status_code != 202:
        print("analyze failed")
        exit()
    print("analyze succeeded")

    poll_method = ARMPolling()
    poller = LROPoller(client._client, response, AnalyzeOperationResult, poll_method)
    result = poller.result()
    print(result)
    for table in result.analyze_result.page_results[0].tables:
        for cell in table.cells:
            print(cell.text)
            print("Cell row span {}".format(cell.row_span)) if cell.row_span else None
            print("Cell column span {}".format(cell.column_span)) if cell.column_span else None
