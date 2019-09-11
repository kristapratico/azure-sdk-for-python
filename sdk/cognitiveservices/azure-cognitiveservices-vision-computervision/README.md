# Azure Computer Vision Python SDK

## Design

The Computer Vision SDK provides a single client that allows you to engage with the Azure Computer Vision API.

The client includes Computer Vision and OCR operations.

Changes:
1. Operations that accept a url and operations that accept an image stream are combined into one operation that takes
    a generic `data` parameter. E.g. analyze_image_in_stream(image, ...) --> analyze_image(data, ...)
2. No longer use CognitiveServicesCredentials from msrest. Now pass in cognitive services key. Need support for AAD?
3. LRO recognize_text() and batch_read_file() return LROPoller's and do the call to get_text_operation_result()
    get_read_operation_result() behind the scenes.
4. Moving from msrest to azure.core we lose params `custom_headers, raw, **operation_config` and gain `cls, **kwargs`.
    cls moved to a kwarg.

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



## ComputerVisionClient API

Changes:
1. Operations that accept a url and operations that accept an image stream are combined into one operation that takes
    a generic `data` parameter. E.g. `analyze_image_in_stream(image, ...)` --> `analyze_image(data, ...)`
2. No longer use `CognitiveServicesCredentials` from msrest. Now pass in cognitive services key. Need support for AAD?
3. LRO `recognize_text()` and `batch_read_file()` return LROPoller's and do the call to `get_text_operation_result()`
    `get_read_operation_result()` behind the scenes.
4. Moving from msrest to azure.core we lose params `custom_headers, raw, **operation_config` and gain `cls, **kwargs`.
    cls moved to a kwarg.
5. analyze_image() broken up into several specific methods: detect_colors, detect_faces, detect_categories,
    detect_adult_content, detect_brands, detect_image_type. analyze_image() unchanged.
6. list_models() returns a `list[ModelDescription]` instead of a `ListModelsResult`
7. tag_image() returns a `list[ImageTag]` instead of a `TagResult`
8. get_area_of_interest() returns a `BoundingRect` instead of `AreaOfInterestResult`
9. detect_objects() now returns a `list[DetectedObject]` instead of `DetectResult`.
10. recognize_text() LROPoller returns a `TextRecognitionResult` instead of `TextOperationResult`.
    Status is now checked with poller object - poller.status()
11. batch_read_file() LROPoller returns a `list[TextRecognitionResult]` instead of `ReadOperationResult`.
    Status is now checked with poller object - poller.status()

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

# Returns list[DetectedObject]
ComputerVisionClient.detect_objects(data, **kwargs)

# Returns ColorInfo
ComputerVisionClient.detect_colors(data, language="en", **kwargs)

# Returns list[FaceDescription]
ComputerVisionClient.detect_faces(data, language="en", **kwargs)

# Returns list[Category]
ComputerVisionClient.detect_categories(data, language="en", details=None, description_exclude=None, **kwargs)

# Returns AdultInfo
ComputerVisionClient.detect_adult_content(data, language="en", **kwargs)

# Returns list[DetectedBrand]
ComputerVisionClient.detect_brands(data, **kwargs)

# Returns ImageType
ComputerVisionClient.detect_image_type(data, language="en", **kwargs)

# Returns list[ModelDescription]
ComputerVisionClient.list_models(**kwargs)

# Returns OcrResult
ComputerVisionClient.recognize_printed_text(data, detect_orientation=True, language="unk", **kwargs)

# Returns list[ImageTag]
ComputerVisionClient.tag_image(data, language="en", **kwargs)

# Returns generator
ComputerVisionClient.generate_thumbnail(data, width, height, smart_cropping=False, **kwargs)

# Returns BoundingRect
ComputerVisionClient.get_area_of_interest(data, **kwargs)

# OCR operations

# Returns an LROPoller. Poller returns TextRecognitionResult
ComputerVisionClient.recognize_text(data, mode, **kwargs)

# Returns an LROPoller. Poller returns list[TextRecognitionResult]
ComputerVisionClient.batch_read_file(data, **kwargs)
```

## Added Scenarios

### 12. Detect colors in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

colors = client.detect_colors(
    data="https://afremov.com/images/product/COLORFUL-NIGHT.jpg",
)

print(colors.dominant_color_foreground)
print(colors.dominant_color_background)
print(colors.dominant_colors)
print(colors.accent_color)
print("Black and white image: ", colors.is_bw_img)
```

### 13. Detect faces in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

faces = client.detect_faces(
    data="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80",
)

for face in faces:
    print(face.age)
    print(face.gender)
    print(face.face_rectangle)
```

### 14. Detect categories in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_categories(
    data="https://image.shutterstock.com/image-vector/cute-cartoon-panda-character-eating-260nw-1050298676.jpg",
)

for category in resp:
    print(category.name, category.score)
```

### 15. Detect adult content in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_adult_content(
    data="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
)

print(resp.is_adult_content, resp.adult_score)
print(resp.is_gory_content, resp.gore_score)
print(resp.is_racy_content, resp.racy_score)
```

### 16. Detect brands in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_brands(
    data="https://di2ponv0v5otw.cloudfront.net/posts/2018/07/05/5b3e96572d8a366433533e80/m_5b3e965b951996f8abec1d42.jpeg",
)

for brand in resp:
    print("Brand found: ", brand.name)
    print("Confidence: ", brand.confidence)
    print("location: ", brand.rectangle)
```

### 17. Detect image type (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_image_type(
    data="https://image.shutterstock.com/image-vector/cute-cartoon-panda-character-eating-260nw-1050298676.jpg",
)

print(resp.clip_art_type)
print(resp.line_drawing_type)
```

## Response type changes

### 18. Changes to list_models()
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

### 19. Changes to tag_image()
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.tag_image(
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg"
)

for tag in resp:
    print(tag.name, tag.confidence)
```

### 20. Changes to get_area_of_interest()
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

result = client.get_area_of_interest(
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

print("x: ", result.x)
print("y: ", result.y)
print("width: ", result.w)
print("height: ", result.h)
```

### 21. Changes to detect_objects()
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_objects(
    data="https://www.leisurepro.com/blog/wp-content/uploads/2012/12/shutterstock_653344564-1366x800@2x.jpg",
)

for obj in resp:
    print("Detected object: ", obj.object_property)
    print("Object location: ", obj.rectangle)  # {x, y, width, height}
    print("Confidence score: ", obj.confidence)
    print("Parent object: ", obj.parent.object_property)
```

### 22. Changes to recognize_text()
```python
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.recognize_text(
    mode="Printed",
    data="http://d2jaiao3zdxbzm.cloudfront.net/wp-content/uploads/figure-65.png",
)

text_result = None
while poller.status() in ["NotStarted", "Running"]:
    time.sleep(1)
    if poller.status() == "Succeeded":
        text_result = poller.result()
    if poller.status() == "Failed":
        print("Oh no")

print("Job completion is: {}\n".format(poller.status()))
print("Recognized:\n")
lines = text_result.lines
for line in lines:
    print(line.text)
```

### 23. Changes to batch_read_file()
```python
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.batch_read_file(data="http://www.historytube.org/wp-content/uploads/2013/07/Declaration-of-Independence-broadside-1776-Jamestown-Yorktown-Foundation2.jpg")
read_result = None
while poller.status() in ["NotStarted", "Running"]:
    time.sleep(1)
    if poller.status() == "Succeeded":
        read_result = poller.result()
    if poller.status() == "Failed":
        print("Oh no")

print("Job completion is: {}\n".format(poller.status()))
print("Recognized:\n")
for image_text in read_result:
    for line in image_text.lines:
        print(line.text)
```