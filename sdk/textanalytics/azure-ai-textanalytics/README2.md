### Single vs. batched method convenience

#### Single text operation

```python
from azure.ai.textanalytics import single_recognize_entities, TextAnalyticsApiKeyCredential

text = "Microsoft was founded by Bill Gates and Paul Allen."

result = single_recognize_entities(
    endpoint=endpoint,
    credential=TextAnalyticsApiKeyCredential(key),
    input_text=text
)

for entity in result.entities:
    print("Entity: {}".format(entity.text))
    print("Type: {}".format(entity.type))
    print("Confidence Score: {}\n".format(entity.score))
```

#### Batch operation passed with single text

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
