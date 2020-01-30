### Single vs. batched method convenience

```python
from azure.ai.textanalytics import single_recognize_entities, TextAnalyticsApiKeyCredential

text = "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975."

result = single_recognize_entities(
    endpoint=endpoint,
    credential=TextAnalyticsApiKeyCredential(key),
    input_text=text,
    language="en"
)

for entity in result.entities:
    print("Entity: {}".format(entity.text))
    print("Type: {}".format(entity.type))
    print("Confidence Score: {}\n".format(entity.score))
```

```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential
    
text_analytics_client = TextAnalyticsClient(endpoint, TextAnalyticsApiKeyCredential(key))

document = ["Microsoft was founded by Bill Gates and Paul Allen."]

result = text_analytics_client.recognize_entities(document)

for entity in result[0].entities:
    print("Entity: {}".format(entity.text))
    print("Type: {}".format(entity.type))
    print("Confidence Score: {}\n".format(entity.score))
```


Track 1 

```python
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
    
text_analytics_client = TextAnalyticsClient(endpoint, CognitiveServicesCredentials(key))

document = [
    {"id": "1", "text": "Microsoft was founded by Bill Gates and Paul Allen."}
]

result = text_analytics_client.entities(document)

for document in result.documents:
    for entity in document.entities:
        print("Entity: {}".format(entity.text))
        print("Type: {}".format(entity.type))
        print("Confidence Score: {}\n".format(entity.score))
```