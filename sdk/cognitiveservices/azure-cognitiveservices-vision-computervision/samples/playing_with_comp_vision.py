import os
from azure.cognitiveservices.vision.computervision.computer_vision_client import ComputerVisionClient
from azure.cognitiveservices.vision.computervision._generated.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import settings_real as settings

IMAGES_FOLDER = "C:\\Users\\krpratic\\azure-sdk-for-python\\sdk\\cognitiveservices\\azure-cognitiveservices-vision-computervision\\samples\\images"


def response_handler(response, deserialized, response_headers):
    return response


def test_analyze_image():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    # resp = client.analyze_image(
    #     data="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
    #     visual_features=[
    #         VisualFeatureTypes.image_type,
    #         VisualFeatureTypes.faces,
    #         VisualFeatureTypes.categories,
    #         VisualFeatureTypes.color,
    #         VisualFeatureTypes.tags,
    #         VisualFeatureTypes.description,
    #     ],
    # )

    with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
        resp = client.analyze_image(
            data=image_stream,
            visual_features=[
                "ImageType",
                "Faces",
                "Categories",
                "Color",
                "Tags",
                "Description",
            ],
        )

    print("This image can be described as: {}\n".format(
        resp.description.captions[0].text))

    print("Tags associated with this image:\nTag\t\tConfidence")
    for tag in resp.tags:
        print("{}\t\t{}".format(tag.name, tag.confidence))

    print("\nThe primary colors of this image are: {}".format(
        resp.color.dominant_colors))


def test_analyze_image_landmarks():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    des = client.analyze_image(
        url="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
        details=["Landmarks"]
    )

    for item in des.categories:
        print(item.detail.landmarks[0].name)


def test_analyze_image_by_domain_landmarks():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    resp = client.analyze_image_by_domain(
        url="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
        model="landmarks"
    )

    for landmark in resp.result["landmarks"]:
        print("Landmark name: ", landmark['name'])
        print("Confidence score: ", landmark['confidence'])

def test_image_analysis_in_stream():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
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
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY
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
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY
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


def test_recognize_text_with_lropoller():
    import time

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    poller = client.recognize_text(
        mode="Printed",
        url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
    )

    text_operation_result = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            text_operation_result = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(text_operation_result.status))
    print("Recognized:\n")
    lines = text_operation_result.recognition_result.lines
    for line in lines:
        print(line.text)


def test_recognize_text():
    import time
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
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


def test_batch_read_file_with_lropoller():
    import time

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    poller = client.batch_read_file(url="http://www.historytube.org/wp-content/uploads/2013/07/Declaration-of-Independence-broadside-1776-Jamestown-Yorktown-Foundation2.jpg")
    read_operation_result = None
    while poller.status() in ["NotStarted", "Running"]:
        time.sleep(1)
        if poller.status() == "Succeeded":
            read_operation_result = poller.result()
        if poller.status() == "Failed":
            print("Oh no")

    print("Job completion is: {}\n".format(read_operation_result.status))
    print("Recognized:\n")
    result = read_operation_result.recognition_results
    for image_text in result:
        for line in image_text.lines:
            print(line.text)


def test_batch_read_file():
    import time
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
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
        credentials=settings.COG_KEY,
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

    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
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


def test_recognize_printed_text():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    with open(
        os.path.join(IMAGES_FOLDER, "text_test2.png"), "rb"
    ) as image_stream:
        image_analysis = client.recognize_printed_text_in_stream(
            image=image_stream,
        )

    print("Printed text recognized:\n")
    for region in image_analysis.regions:
        for line in region.lines:
            line_text = " ".join([word.text for word in line.words])
            print(line_text)

    print("Language: ", image_analysis.language)
    print("Angle of detected text: ", image_analysis.text_angle)
    print("Orientation of detected text: ", image_analysis.orientation)


def test_recognize_printed_text_in_stream():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
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
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    resp = client.describe_image(
        url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg",
        max_candidates=3
    )

    print(resp.tags)  # list[str] of tags
    for caption in resp.captions:
        print(caption.text, caption.confidence)


def test_detect_object():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    resp = client.detect_objects(
        url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
    )

    for obj in resp.objects:
        print("Detected object: ", obj.object_property)
        print("Object location: ", obj.rectangle)  # {x, y, width, height}
        print("Confidence score: ", obj.confidence)
        print("Parent object: ", obj.parent.object_property)


def test_detect_object_in_stream():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
        image_analysis = client.detect_objects_in_stream(
            image=image_stream,
        )

    for obj in image_analysis.objects:
        print(obj)


def test_list_models():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    models = client.list_models()
    for model in models.models_property:
        print(model.name, model.categories)


def test_tag_image_in_stream():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )
    with open(
        os.path.join(IMAGES_FOLDER, "house.jpg"), "rb"
    ) as image_stream:
        resp = client.tag_image_in_stream(
            image=image_stream,
        )

    for tag in resp.tags:
        print(tag.name, tag.confidence)


def test_generate_thumbnail():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    thumb = client.generate_thumbnail(
        url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
        width=100,
        height=100,
    )

    with open("my_thumbnail.jpeg", "wb") as img:
        for byt in thumb:
            img.write(byt)


def test_get_area_of_interest():
    client = ComputerVisionClient(
        endpoint="https://westus2.api.cognitive.microsoft.com/",
        credentials=settings.COG_KEY,
    )

    result = client.get_area_of_interest(
        url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
    )

    print("x: ", result.area_of_interest.x)
    print("y: ", result.area_of_interest.y)
    print("width: ", result.area_of_interest.w)
    print("height: ", result.area_of_interest.h)
