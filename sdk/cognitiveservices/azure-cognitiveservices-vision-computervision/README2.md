# Azure Computer Vision Python SDK

## Design

The Computer Vision SDK provides a single client that allows you to engage with the Azure Computer Vision API.

The client includes Computer Vision and OCR operations.

## ComputerVisionClient API

Changes:
1. Operations that accept a url and operations that accept an image stream are combined into one operation that takes
    an `image_or_url` parameter. E.g. analyze_image_in_stream(image, ...) --> analyze_image(image_or_url, ...)
2. No longer use CognitiveServicesCredentials from msrest. Pass credential parameter string into client as the 
    cognitive services account key or Azure Active Directory credentials.
3. LRO recognize_text() is being deprecated and will not be included in the sdk.
4. LRO batch_read_file() will return a polling object and do the calls to get_read_operation_result() internally. 
    User checks operation status with the poller object. batch_read_file() will return a 
    `list[TextRecognitionResult]` instead of `ReadOperationResult`.
5. The operations which read characters/text from an image (recognize_printed_text, batch_read_file)
    will include an extra param in the model returned called `full_text`. This will contain all the text recognized
    as a string. This makes workflows in which text data is passed into text analytics, etc. services more seamless.
6. Re-locate metadata and request_id to response hook to help simplify the models returned:
    - detect_objects() returns `list[DetectedObject]` instead of `DetectResult`
    - list_models() returns a `list[ModelDescription]` instead of `ListModelsResult`
    - tag_image() returns a `list[ImageTag]` instead of a `TagResult`
    - get_area_of_interest() returns a `BoundingRect` instead of a `AreaOfInterestResult`
    - analyze_image_by_domain() returns a `list[dict{name, confidence}]` instead of a `DomainModelResult`
7. Since image tags can be returned from tag_image(), let's not return them for describe_image() as well. 
    We can further simplify the response by sending metadata and request ID to response hook. 
    So describe_image() will return a `list[ImageCaption]` instead of `ImageDescription`.
8. Parameter `description_exclude` moved to kwargs for analyze_image() and describe_image()


```python
azure.cognitiveservices.vision.computervision.ComputerVisionClient(endpoint, credentials)


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

# Returns an LROPoller. Poller returns list[TextRecognitionResult]
ComputerVisionClient.batch_read_file(image_or_url, **kwargs)

------------------------------------------------------------------------------------------------------------------------
# Added Operations

# Returns ColorInfo
ComputerVisionClient.detect_colors(image_or_url, language="en", **kwargs)

# Returns list[FaceDescription]
ComputerVisionClient.detect_faces(image_or_url, language="en", **kwargs)

# Returns list[Category]
ComputerVisionClient.categorize_image(image_or_url, details=None, language="en", **kwargs)

# Returns AdultInfo
ComputerVisionClient.detect_adult_content(image_or_url, language="en", **kwargs)

# Returns list[DetectedBrand]
ComputerVisionClient.detect_brands(image_or_url, **kwargs)

# Returns ImageType
ComputerVisionClient.detect_image_type(image_or_url, language="en", **kwargs)
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
    smart_cropping=True
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

### 10. Recognize text in a text heavy image or a batch of images/pdf files (long running operation).
```python
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

poller = client.batch_read_file(image_or_url="http://www.historytube.org/wp-content/uploads/2013/07/Declaration-of-Independence-broadside-1776-Jamestown-Yorktown-Foundation2.jpg")
read_result = None
while poller.status() in ["NotStarted", "Running", "Succeeded"]:
    if poller.status() == "Succeeded":
        read_result = poller.result()
        break
    if poller.status() == "Failed":
        print("Oh no")

print("Job completion is: {}\n".format(poller.status()))

print("Recognized full text, page 1:\n")
print(read_result[0].full_text)

print("Recognized text line-by-line:\n")
for image_text in read_result:
    for line in image_text.lines:
        print(line.text)
```

## Added Scenarios

### 11. Detect colors in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

colors = client.detect_colors(
    image_or_url="https://afremov.com/images/product/COLORFUL-NIGHT.jpg",
)

print(colors.dominant_color_foreground)
print(colors.dominant_color_background)
print(colors.dominant_colors)
print(colors.accent_color)
print("Black and white image: ", colors.is_bw_img)
```

### 12. Detect faces in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

faces = client.detect_faces(
    image_or_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80",
)

for face in faces:
    print(face.age)
    print(face.gender)
    print(face.face_rectangle)
```

### 13. Detect categories in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.categorize_image(
    image_or_url="https://image.shutterstock.com/image-vector/cute-cartoon-panda-character-eating-260nw-1050298676.jpg",
)

for category in resp:
    print(category.name, category.score)
```

### 14. Detect adult content in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_adult_content(
    image_or_url="https://cdn.vox-cdn.com/thumbor/2obROpfYnG3r83wV-puexZi-3nQ=/0x0:2971x1939/1200x800/filters:focal(1272x316:1746x790)/cdn.vox-cdn.com/uploads/chorus_image/image/55253763/11364550914_521e079ff7_o_d.1497454023.jpg",
)

print(resp.is_adult_content, resp.adult_score)
print(resp.is_gory_content, resp.gore_score)
print(resp.is_racy_content, resp.racy_score)
```

### 15. Detect brands in an image (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_brands(
    image_or_url="https://di2ponv0v5otw.cloudfront.net/posts/2018/07/05/5b3e96572d8a366433533e80/m_5b3e965b951996f8abec1d42.jpeg",
)

for brand in resp:
    print("Brand found: ", brand.name)
    print("Confidence: ", brand.confidence)
    print("location: ", brand.rectangle)
```

### 16. Detect image type (url or upload)
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient

client = ComputerVisionClient(
    endpoint="https://westus2.api.cognitive.microsoft.com/",
    credentials="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
)

resp = client.detect_image_type(
    image_or_url="https://image.shutterstock.com/image-vector/cute-cartoon-panda-character-eating-260nw-1050298676.jpg",
)

print(resp.clip_art_type)
print(resp.line_drawing_type)
```