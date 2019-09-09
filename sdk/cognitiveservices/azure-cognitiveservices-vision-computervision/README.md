# Azure Computer Vision Python SDK

## Design

The Computer Vision SDK provides a single client that allows you to engage with the Azure Computer Vision API.

The client includes Computer Vision and OCR operations.


## ComputerVisionClient API
```python
azure.cognitiveservices.vision.computervision.ComputerVisionClient(endpoint, credentials)

# Computer Vision operations

# Returns ImageAnalysis
ComputerVisionClient.analyze_image(
    data, visual_features=None, details=None, language="en", description_exclude=None, **kwargs)

# Returns DomainModelResults
ComputerVisionClient.analyze_image_by_domain(data, model, language="en", **kwargs)

# Returns ImageDescription
ComputerVisionClient.describe_image(data, max_candidates=1, language="en", description_exclude=None, **kwargs)

# Returns DetectResult
ComputerVisionClient.detect_objects(data, **kwargs)

# Returns ListModelsResult
ComputerVisionClient.list_models(**kwargs)

# Returns OcrResult
ComputerVisionClient.recognize_printed_text(data, detect_orientation=True, language="unk", **kwargs)

# Returns TagResult
ComputerVisionClient.tag_image(data, language="en", **kwargs)

# Returns generator
ComputerVisionClient.generate_thumbnail(data, width, height, smart_cropping=False, **kwargs)

# Returns AreaOfInterestResult
ComputerVisionClient.get_area_of_interest(data, **kwargs)

# OCR operations

# Returns an LROPoller. Poller returns TextOperationResult
ComputerVisionClient.recognize_text(data, mode, **kwargs)

# Returns an LROPoller. Poller returns ReadOperationResult.
ComputerVisionClient.batch_read_file(data, **kwargs)
```

## Scenarios

### 1. Analyze an image (url or upload) for visual features
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

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
```

### 2. Analyze an image (url or upload) based on a domain specific model (landmarks or celebrities)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.analyze_image_by_domain(
    data="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
    model="landmarks"
)

for landmark in resp.result["landmarks"]:
    print("Landmark name: ", landmark['name'])
    print("Confidence score: ", landmark['confidence'])
```

### 3. Describe an image (url or upload) in human readable language with complete sentences.
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.describe_image(
    data="https://images2.minutemediacdn.com/image/upload/c_crop,h_1193,w_2121,x_0,y_64/f_auto,q_auto,w_1100/v1565279671/shape/mentalfloss/578211-gettyimages-542930526.jpg",
)

print("Tags associated: ", resp.tags)  # list[str] of tags
for caption in resp.captions:
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
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

for obj in resp.objects:
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
for model in models.models_property:
    print(model.name, model.categories)
```

### 6. Detects printed text in an image (url or upload).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

with open(
    os.path.join(IMAGES_FOLDER, "text_test2.png"), "rb"
) as image_stream:
    image_analysis = client.recognize_printed_text(
        data=image_stream,
    )

print("Printed text recognized:\n")
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
with open(
    os.path.join(IMAGES_FOLDER, "house.jpg"), "rb"
) as image_stream:
    resp = client.tag_image(
        data=image_stream,
    )

for tag in resp.tags:
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
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
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
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

print("x: ", result.area_of_interest.x)
print("y: ", result.area_of_interest.y)
print("width: ", result.area_of_interest.w)
print("height: ", result.area_of_interest.h)
```

### 10. Recognize text in an image (long running operation).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.recognize_text(
    mode="Printed",
    data="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
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
```

### 11. Recognize text in a text heavy image (long running operation).
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.batch_read_file(
    data="http://www.historytube.org/wp-content/uploads/2013/07/Declaration-of-Independence-broadside-1776-Jamestown-Yorktown-Foundation2.jpg"
)

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
```

