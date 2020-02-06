import os
import time
from azure.cognitiveservices.formrecognizer import FormRecognizerClient


def response_handler(resp, re, headers):
    return resp

# endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
# key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def testing_receipt():
    client = FormRecognizerClient(endpoint=endpoint, credentials=key)

    response = client.analyze_receipt_async(
        include_text_details=True,
        file_stream={"source": "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/contoso-allinone.jpg"},
        headers={"Ocp-Apim-Subscription-Key": key},
        cls=response_handler)


    if response.status_code != 202:
        print("analyze failed:\n%s" % response.text)
        exit()
    print("analyze succeeded:\n%s" % response.headers)
    operation_id = response.headers["Operation-Location"]
    op_location_id = operation_id.split("analyzeResults/")[1]

    result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key})
    time.sleep(5)
    while result.status != "succeeded":
        result = client.get_analyze_receipt_result(op_location_id, headers={"Ocp-Apim-Subscription-Key": key}, cls=response_handler)

    print(result)



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
