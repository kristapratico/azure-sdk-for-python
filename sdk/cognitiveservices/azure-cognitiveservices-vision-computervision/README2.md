# Azure Computer Vision Python SDK

## Design

The Computer Vision SDK provides a single client that allows you to engage with the Azure Computer Vision API.

The client includes Computer Vision and OCR operations.

## ComputerVisionClient API

Changes:
1. Operations that accept a url and operations that accept an image stream are combined into one operation that takes
    an `image_or_url` parameter. E.g. analyze_image_in_stream(image, ...) --> analyze_image(image_or_url, ...)
2. No longer use CognitiveServicesCredentials from msrest. Now pass credential parameter which can be the cognitive
    services account key or Azure Active Directory credentials.
3. LRO recognize_text() and batch_read_file() return LROPoller's and do the call to get_text_operation_result() and
    get_read_operation_result() internally. User checks operation status with the poller object. Response changes:
    recognize_text() returns a `TextRecognitionResult` instead of `TextOperationResult`. batch_read_file() returns a 
    `list[TextRecognitionResult]` instead of `ReadOperationResult`.
4. Re-locate metadata and request_id to response hook to help simplify the models returned:
    - detect_objects() returns `list[DetectedObject]` instead of `DetectResult`
    - list_models() returns a `list[ModelDescription]` instead of `ListModelsResult`
    - tag_image() returns a `list[ImageTag]` instead of a `TagResult`
    - get_area_of_interest() returns a `BoundingRect` instead of a `AreaOfInterestResult`
5. Since image tags can be returned from tag_image(), let's not return them for describe_image() as well. 
    We can further simplify the response by sending metadata and request ID to response hook. 
    So describe_image() will return a `list[ImageCaption]` instead of `ImageDescription`.
6. Parameter `description_exclude` moved to kwargs for analyze_image() and describe_image()
7. For analyze_image_by_domain(), move metadata and request_id to response hook and simplify response by removing
    outer dictionary. Response changed to `list[dict{name, confidence}]` from `DomainModelResult`. We could create
    a new model to make this return type less generic? `list[DomainResult]`?
8. The operations which read characters/text from an image (recognize_text, recognize_printed_text, batch_read_file)
    will include an extra param in the model returned called `full_text`. This will contain all the text recognized
    as a string. This makes workflows in which OCR data is passed into text analytics services more seamless.

```python
azure.cognitiveservices.vision.computervision.ComputerVisionClient(endpoint, credentials)

# Computer Vision operations

# Returns ImageAnalysis
ComputerVisionClient.analyze_image(
    image_or_url, visual_features=None, details=None, language="en", **kwargs)

# Returns list[dict{name:, confidence:}]
ComputerVisionClient.analyze_image_by_domain(image_or_url, model, language="en", **kwargs)

# Returns list[ImageCaption]
ComputerVisionClient.describe_image(image_or_url, max_candidates=1, language="en", **kwargs)

# Returns list[DetectedObject]
ComputerVisionClient.detect_objects(image_or_url, **kwargs)

# Returns list[ModelDescription]
ComputerVisionClient.list_models(**kwargs)

# Returns OcrResult
ComputerVisionClient.recognize_printed_text(image_or_url, detect_orientation=True, language="unk", **kwargs)

# Returns list[ImageTag]
ComputerVisionClient.tag_image(image_or_url, language="en", **kwargs)

# Returns generator
ComputerVisionClient.generate_thumbnail(image_or_url, width, height, smart_cropping=False, **kwargs)

# Returns BoundingRect
ComputerVisionClient.get_area_of_interest(image_or_url, **kwargs)

# OCR operations

# Returns an LROPoller. Poller returns TextRecognitionResult
ComputerVisionClient.recognize_text(image_or_url, mode, **kwargs)

# Returns an LROPoller. Poller returns list[TextRecognitionResult]
ComputerVisionClient.batch_read_file(image_or_url, **kwargs)
```

## Scenarios

### 1. Analyze an image (url or upload) for multiple visual features
```python
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient


client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

with open(os.path.join(IMAGES_FOLDER, "house.jpg"), "rb") as image_stream:
    resp = client.analyze_image(
        image_or_url=image_stream,
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
```

### 2. Analyze an image (url or upload) based on a domain specific model (landmarks or celebrities)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.analyze_image_by_domain(
    image_or_url="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
    model="landmarks"
)

for landmark in resp:
    print(landmark['name'])
    print(landmark['confidence'])
```

### 3. Describe an image (url or upload) in human readable language with complete sentences.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.describe_image(
    image_or_url="https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg",
)

for caption in resp:
    print(caption.text, caption.confidence)
```

### 4. Detect objects in an image (url or upload).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_objects(
    image_or_url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

for obj in resp:
    print("Detected object: ", obj.object_property)
    print("Object location: ", obj.rectangle)  # {x, y, width, height}
    print("Confidence score: ", obj.confidence)
    print("Parent object: ", obj.parent.object_property)
```

### 5. List the domain-specific models that are supported by the Computer Vision API.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

models = client.list_models()
for model in models:
    print(model.name, model.categories)
```

### 6. Detects printed text in an image (url or upload).
```python
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

with open(
    os.path.join(IMAGES_FOLDER, "text_test2.png"), "rb"
) as image_stream:
    image_analysis = client.recognize_printed_text(
        image_or_url=image_stream,
    )

print("Printed full text recognized:\n")
print(image_analysis.full_text)

print("Printed text line-by-line")
for region in image_analysis.regions:
    for line in region.lines:
        line_text = " ".join([word.text for word in line.words])
        print(line_text)

print("Language: ", image_analysis.language)
print("Angle of detected text: ", image_analysis.text_angle)
print("Orientation of detected text: ", image_analysis.orientation)
```

### 7. Generate a list of words, or tags, that are relevant to the content of the supplied image (url or upload).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.tag_image(
    image_or_url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg"
)

for tag in resp:
    print(tag.name, tag.confidence)
```

### 8. Generate a thumbnail image with the user-specified width and height from a supplied image (url or upload).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

thumb = client.generate_thumbnail(
    image_or_url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
    width=100,
    height=100,
)

with open("my_thumbnail.jpeg", "wb") as img:
    for byt in thumb:
        img.write(byt)
```

### 9. Get a bounding box around the most important area of the image.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

result = client.get_area_of_interest(
    image_or_url="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

print("x: ", result.x)
print("y: ", result.y)
print("width: ", result.w)
print("height: ", result.h)
```

### 10. Recognize text in an image (long running operation).
```python
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.recognize_text(
    mode="Printed",
    image_or_url="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
)

text_result = None
while poller.status() in ["NotStarted", "Running"]:
    time.sleep(1)
    if poller.status() == "Succeeded":
        text_result = poller.result()
    if poller.status() == "Failed":
        print("Oh no")

print("Job completion is: {}\n".format(poller.status()))

print("Recognized full text:\n")
print(text_result.full_text)

print("Recognized text line-by-line:\n")
lines = text_result.lines
for line in lines:
    print(line.text)
```

### 11. Recognize text in a text heavy image or a batch of images/pdf files (long running operation).
```python
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.batch_read_file(image_or_url="http://www.historytube.org/wp-content/uploads/2013/07/Declaration-of-Independence-broadside-1776-Jamestown-Yorktown-Foundation2.jpg")
read_result = None
while poller.status() in ["NotStarted", "Running"]:
    time.sleep(1)
    if poller.status() == "Succeeded":
        read_result = poller.result()
    if poller.status() == "Failed":
        print("Oh no")

print("Job completion is: {}\n".format(poller.status()))

print("Recognized full text:\n")
print(read_result.full_text)

print("Recognized text line-by-line:\n")
for image_text in read_result:
    for line in image_text.lines:
        print(line.text)
```
