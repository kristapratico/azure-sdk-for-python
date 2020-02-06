import os
import time



endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def response_handler(response, _, response_headers):
    return response

def testing_receipt():
    from azure.core.polling import LROPoller
    from azure.cognitiveservices.formrecognizer import FormRecognizerClient
    from azure.cognitiveservices.formrecognizer.models import AnalyzeOperationResult, AnalyzeResult
    from azure.mgmt.core.polling.arm_polling import ARMPolling

    client = FormRecognizerClient(endpoint=endpoint, credentials=key)

    response = client.analyze_receipt_async(
        file_stream={"source": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"},
        include_text_details=True,
        cls=response_handler)

    if response.status_code != 202:
        print("analyze failed")
        exit()
    print("analyze succeeded")

    response.http_response = response
    poll_method = ARMPolling()
    poller = LROPoller(client._client, response, AnalyzeResult, poll_method)
    status = poller.status()
    while status.lower() != "succeeded":
        status = poller.status()
    result = poller.result()
    print(result)




    # while poller.status() in ["NotStarted", "Running", "Succeeded"]:
    #     if poller.status() == "Succeeded":
    #         result = poller.result()
    #         break
    #     if poller.status() == "Failed":
    #         print("Oh no")
    # operation_id = response.headers["Operation-Location"]
    # op_location_id = operation_id.split("analyzeResults/")[1]
    #
    # result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key})
    # time.sleep(5)
    # while result.status != "succeeded":
    #     result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key}, cls=response_handler)

def testing_layout():
    client = FormRecognizerClient(endpoint=endpoint, credentials=key)

    response = client.analyze_layout_async(
        file_stream={"source": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"},
        headers={"Ocp-Apim-Subscription-Key": key},
        cls=response_handler)

    time.sleep(2)
    if response.status_code != 202:
        print("analyze failed:\n%s" % response.text)
        exit()
    print("analyze succeeded:\n%s" % response.headers)
    operation_id = response.headers["Operation-Location"]
    op_location_id = operation_id.split("analyzeResults/")[1]

    result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key})
    while result.status != "succeeded":
        result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key}, cls=response_handler)

    print(result)
