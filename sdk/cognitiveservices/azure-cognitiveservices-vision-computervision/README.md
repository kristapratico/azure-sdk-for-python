# Azure Computer Vision Python SDK

## Design

The Computer Vision SDK provides a single client that allows you to engage with the Azure Computer Vision API.
This includes both Computer Vision and OCR operations. The client is created with an `endpoint` and `credential`.
The `credential` can be the user's Cognitive Services/Computer Vision account key or a token credential from 
Azure Active Directory.

To simplify the SDK, methods that accept an image URL and methods that accept an image stream are combined into
one that takes an `image_or_url` parameter. For example, `analyze_image(url, ...)` and 
`analyze_image_in_stream(image, ...)` become 
`analyze_image(image_or_url, ...)` and passes the input to the correct API call. 

Additional design changes described below.

Some methods removed:
* recognize_text() is being deprecated and won't be included in the SDK.
* list_models() removed since no new classifiers will be added. 

Renames:
* tag_image() renamed to list_image_tags()
* batch_read_file() renamed to batch_recognize_text()
* analyze_image() parameter `details` renamed to `models`
* get_area_of_interest() renamed to identify_region_of_interest()
* `BoundingRect` renamed to `BoundingBox`

Some parameters move to **kwargs: 
* `language` moves to kwargs for analyze_image(), analyze_image_by_domain(), describe_image(), list_image_tags().
* `description_exclude` move to kwargs for analyze_image() and describe_image().

`metadata` and `request_id` relocated to response hook to help simplify the models returned:
- detect_objects() returns `list[DetectedObject]` instead of `DetectResult`
- list_image_tags() returns a `list[ImageTag]` instead of a `TagResult`
- identify_region_of_interest() returns a `BoundingBox` instead of a `AreaOfInterestResult`
- analyze_image_by_domain() returns a `list[dict{name, confidence}]` instead of a `DomainModelResult`

Improvements to OCR operations:
* batch_recognize_text() will return a polling object which does the calls to get_read_operation_result() internally. 
    User will check the operation status on the poller object. 
    This will allow batch_recognize_text() to return a `list[TextRecognitionResult]` instead of `ReadOperationResult`.
* recognize_printed_text() and batch_recognize_text() will include an extra param in the returned model 
    called `full_text`. This will contain all the text recognized as a string.

```python
azure.cognitiveservices.vision.computervision.ComputerVisionClient(endpoint, credential)


# Returns ImageAnalysis
ComputerVisionClient.analyze_image(
    image_or_url, visual_features=None, models=None, **kwargs)

# Returns list[dict{name, confidence}]
ComputerVisionClient.analyze_image_by_domain(image_or_url, model, **kwargs)

# Returns ImageDescription
ComputerVisionClient.describe_image(image_or_url, max_candidates=1, **kwargs)

# Returns list[DetectedObject]
ComputerVisionClient.detect_objects(image_or_url, **kwargs)

# Returns OcrResult
ComputerVisionClient.recognize_printed_text(image_or_url, detect_orientation=True, language="unk", **kwargs)

# Returns list[ImageTag]
ComputerVisionClient.list_image_tags(image_or_url, **kwargs)

# Returns generator
ComputerVisionClient.generate_thumbnail(image_or_url, width, height, smart_cropping=False, **kwargs)

# Returns BoundingBox
ComputerVisionClient.identify_region_of_interest(image_or_url, **kwargs)

# Returns an LROPoller. Poller returns list[TextRecognitionResult]
ComputerVisionClient.batch_recognize_text(image_or_url, **kwargs)
```

## Scenarios

### 1. Analyze an image for multiple visual features
```python
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient


client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
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

### 2. Analyze an image based on a domain specific model (landmarks or celebrities)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.analyze_image_by_domain(
    image_or_url="https://image.jpg",
    model="landmarks"
)

for landmark in resp:
    print(landmark['name'])
    print(landmark['confidence'])
```

### 3. Describe an image in human readable language with complete sentences.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.describe_image(image_or_url="https://image.jpg")

for caption in resp.captions:
    print(caption.text, caption.confidence)
```

### 4. Detect objects in an image.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_objects(image_or_url="https://image.jpg")

for obj in resp:
    print("Detected object: ", obj.object_property)
    print("Object location: ", obj.rectangle)  # {x, y, width, height}
    print("Confidence score: ", obj.confidence)
    print("Parent object: ", obj.parent.object_property)
```

### 5. Detect printed text in an image.
```python
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

with open(
    os.path.join(IMAGES_FOLDER, "text_test.png"), "rb"
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

### 6. Generate a list of words, or tags, that are relevant to the content of the supplied image.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.list_image_tags(image_or_url="https://image.jpg")

for tag in resp:
    print(tag.name, tag.confidence)
```

### 7. Generate a thumbnail image with the user-specified width and height from a supplied image.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

thumb = client.generate_thumbnail(
    image_or_url="https://image.jpg",
    width=100,
    height=100,
    smart_cropping=True
)

with open("my_thumbnail.jpeg", "wb") as img:
    for byt in thumb:
        img.write(byt)
```

### 8. Get a bounding box around the most important area of the image.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

result = client.identify_region_of_interest(image_or_url="https://image.jpg")

print("x: ", result.x)
print("y: ", result.y)
print("width: ", result.w)
print("height: ", result.h)
```

### 9. Recognize text in a text heavy image or a batch of images/pdf files (long running operation).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.batch_recognize_text(image_or_url="https://image_text.jpg")

while poller.status() in ["NotStarted", "Running", "Succeeded"]:
    if poller.status() == "Succeeded":
        read_result = poller.result()
        break
    if poller.status() == "Failed":
        raise Exception

print("Job completion is: {}\n".format(poller.status()))

print("Recognized full text, page 1:\n")
print(read_result[0].full_text)

print("Recognized text line-by-line:\n")
for image_text in read_result:
    for line in image_text.lines:
        print(line.text)
```

### Extra example - retrieve request_id and metadata from response hook
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credential="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

response_data = []
def callback(response):
    response_data.append(response.metadata)
    response_data.append(response.request_id)

resp = client.list_image_tags(image_or_url="https://image.jpg")

for tag in resp:
    print(tag.name, tag.confidence)
```


