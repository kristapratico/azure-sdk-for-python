import os
from azure.cognitiveservices.vision.computervision.computer_vision_client import ComputerVisionClient
from azure.cognitiveservices.vision.computervision._generated.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

IMAGES_FOLDER = "C:\\Users\\krpratic\\azure-sdk-for-python\\sdk\\cognitiveservices\\azure-cognitiveservices-vision-computervision\\samples\\images"


def response_handler(response, deserialized, response_headers):
    return response


def test_analyze_image():
    credential = "d926defc24d24403ac6252b360aa6ab2"
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    des = client.analyze_image(
        url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg",
        visual_features=[
            VisualFeatureTypes.image_type,
            VisualFeatureTypes.faces,
            VisualFeatureTypes.categories,
            VisualFeatureTypes.color,
            VisualFeatureTypes.tags,
            VisualFeatureTypes.description,
        ],
    )

    for item in des.categories:
        print(item)

    print(des.metadata)


def test_image_analysis_in_stream():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
        image_analysis = client.analyze_image_in_stream(
            image=image_stream,
            visual_features=[
                VisualFeatureTypes.image_type,
                VisualFeatureTypes.faces,
                VisualFeatureTypes.categories,
                VisualFeatureTypes.color,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.description,
            ],
        )

    for cat in image_analysis.categories:
        print(cat)
    print(
        "This image can be described as: {}\n".format(
            image_analysis.description.captions[0].text
        )
    )

    print("Tags associated with this image:\nTag\t\tConfidence")
    for tag in image_analysis.tags:
        print("{}\t\t{}".format(tag.name, tag.confidence))

    print(
        "\nThe primary colors of this image are: {}".format(
            image_analysis.color.dominant_colors
        )
    )


def recognize_text_in_stream_using_lropoller():
    import time
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential
    )

    with open(
        os.path.join(IMAGES_FOLDER, "make_things_happen.jpg"), "rb"
    ) as image_stream:
        poller = client.recognize_text_in_stream(
            image=image_stream,
            mode="Printed",
        )

    result = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            result = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(result.status))
    print("Recognized:\n")
    lines = result.recognition_result.lines
    print(lines[0].words[0].text)  # "make"
    print(lines[1].words[0].text)  # "things"
    print(lines[2].words[0].text)  # "happen"


def test_recognize_text_in_stream():
    import time
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential
    )

    with open(
        os.path.join(IMAGES_FOLDER, "make_things_happen.jpg"), "rb"
    ) as image_stream:
        job = client.recognize_text_in_stream(
            image=image_stream,
            mode="Printed",
            cls=response_handler
        )

    operation_id = job.headers["Operation-Location"].split("/")[-1]

    image_analysis = client.get_text_operation_result(operation_id)

    while image_analysis.status in ["NotStarted", "Running"]:
        time.sleep(1)
        image_analysis = client.get_text_operation_result(
            operation_id=operation_id,
        )

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    lines = image_analysis.recognition_result.lines
    print(lines[0].words[0].text)  # "make"
    print(lines[1].words[0].text)  # "things"
    print(lines[2].words[0].text)  # "happen"


def recognize_text_with_lropoller():
    import time

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials="d926defc24d24403ac6252b360aa6ab2",
    )

    poller = client.recognize_text(
        mode="Printed",
        url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
    )

    image_analysis = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            image_analysis = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    lines = image_analysis.recognition_result.lines
    for line in lines:
        print(line.text)


def test_recognize_text():
    import time
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    job = client.recognize_text(
        mode="Printed",
        url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
        cls=response_handler
    )

    operation_id = job.headers["Operation-Location"].split("/")[-1]

    image_analysis = client.get_text_operation_result(operation_id)

    while image_analysis.status in ["NotStarted", "Running"]:
        time.sleep(1)
        image_analysis = client.get_text_operation_result(
            operation_id=operation_id,
        )

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    lines = image_analysis.recognition_result.lines
    for line in lines:
        print(line.text)


def batch_read_file_with_lropoller():
    import time

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials="d926defc24d24403ac6252b360aa6ab2",
    )

    poller = client.batch_read_file(url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png")
    image_analysis = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            image_analysis = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    result = image_analysis.recognition_results
    for line in result[0].lines:
        print(line.text)


def test_batch_read_file():
    import time
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    job = client.batch_read_file(url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
                                 cls=response_handler)

    operation_id = job.headers["Operation-Location"].split("/")[-1]

    image_analysis = client.get_read_operation_result(operation_id)

    while image_analysis.status in ["NotStarted", "Running"]:
        time.sleep(1)
        image_analysis = client.get_read_operation_result(
            operation_id=operation_id,
        )

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    result = image_analysis.recognition_results
    for line in result[0].lines:
        print(line.text)


def test_batch_read_file_in_stream_with_lropoller():
    import time

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials="d926defc24d24403ac6252b360aa6ab2",
    )

    with open(
        os.path.join(IMAGES_FOLDER, "computer_vision_ocr.png"), "rb"
    ) as image_stream:
        poller = client.batch_read_file_in_stream(
            image=image_stream,
        )

    image_analysis = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            image_analysis = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    result = image_analysis.recognition_results
    for line in result[0].lines:
        print(line.text)


def test_batch_read_file_in_stream():
    import time
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    with open(
        os.path.join(IMAGES_FOLDER, "computer_vision_ocr.png"), "rb"
    ) as image_stream:
        job = client.batch_read_file_in_stream(
            image=image_stream,
            cls=response_handler
        )

    operation_id = job.headers["Operation-Location"].split("/")[-1]

    image_analysis = client.get_read_operation_result(operation_id)

    while image_analysis.status in ["NotStarted", "Running"]:
        time.sleep(1)
        image_analysis = client.get_read_operation_result(
            operation_id=operation_id,
        )

    print("Job completion is: {}\n".format(image_analysis.status))
    print("Recognized:\n")
    result = image_analysis.recognition_results
    for line in result[0].lines:
        print(line.text)


def test_recognize_printed_text_in_stream():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    with open(
        os.path.join(IMAGES_FOLDER, "computer_vision_ocr.png"), "rb"
    ) as image_stream:
        image_analysis = client.recognize_printed_text_in_stream(
            image=image_stream,
            language="en",
        )

    lines = image_analysis.regions[0].lines
    print("Recognized:\n")
    for line in lines:
        line_text = " ".join([word.text for word in line.words])
        print(line_text)


def test_describe_image():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    des = client.describe_image(
        url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg",
    )

    for cap in des.captions:
        print(cap.text, cap.confidence)
    print(des.captions)


def test_detect_object():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    des = client.detect_objects(
        url="https://hips.hearstapps.com/ame-prod-goodhousekeeping-assets.s3.amazonaws.com/main/embedded/29857/three-kittens.jpg?resize=480:*",
    )

    des2 = client.detect_objects(
        url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
    )

    for obj in des2.objects:
        print(obj)


def test_detect_object_in_stream():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )

    with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
        image_analysis = client.detect_objects_in_stream(
            image=image_stream,
        )

    for obj in image_analysis.objects:
        print(obj)


def test_list_models():
    credential = CognitiveServicesCredentials("d926defc24d24403ac6252b360aa6ab2")
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )
    models = client.list_models()
    print(models.models_property)
    for mod in models.models_property:
        print(mod)


def test_tag_image_in_stream():
    credential = "d926defc24d24403ac6252b360aa6ab2"
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=credential,
    )
    with open(
        os.path.join(IMAGES_FOLDER, "house.jpg"), "rb"
    ) as image_stream:
        tag_result = client.tag_image_in_stream(
            image=image_stream,
        )

    print(tag_result)
    for tag in tag_result.tags:
        print(tag)

