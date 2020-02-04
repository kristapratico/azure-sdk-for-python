# Single vs. batched method convenience

## Recognize Entities

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


## Analyze Sentiment

#### Single text operation

```python
from azure.ai.textanalytics import single_analyze_sentiment, TextAnalyticsApiKeyCredential

text = "I hated that restuarant. The food was awful."

result = single_analyze_sentiment(
    endpoint=endpoint,
    credential=TextAnalyticsApiKeyCredential(key),
    input_text=text
)

print("Overall sentiment: {}".format(result.sentiment))
print("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
    result.document_scores.positive,
    result.document_scores.neutral,
    result.document_scores.negative,
))
```

#### Batch operation passed with single text

```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

text_analytics_client = TextAnalyticsClient(endpoint, TextAnalyticsApiKeyCredential(key))

document = ["I hated that restuarant. The food was awful."]

result = text_analytics_client.analyze_sentiment(document)

print("Overall sentiment: {}".format(result[0].sentiment))
print("Overall scores: positive={0:.3f}; neutral={1:.3f}; negative={2:.3f} \n".format(
    result[0].sentiment_scores.positive,
    result[0].sentiment_scores.neutral,
    result[0].sentiment_scores.negative,
))
```

## Extract Key Phrases

#### Single text operation

```python
from azure.ai.textanalytics import single_extract_key_phrases, TextAnalyticsApiKeyCredential

text = "Redmond is a city in King County, Washington, United States, located 15 miles east of Seattle."

result = single_extract_key_phrases(
    endpoint=endpoint,
    credential=TextAnalyticsApiKeyCredential(key),
    input_text=text
)

print("Key phrases found:\n")
for phrase in result.key_phrases:
    print(phrase)
```

#### Batch operation passed with single text

```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

text_analytics_client = TextAnalyticsClient(endpoint, TextAnalyticsApiKeyCredential(key))

document = ["I hated that restuarant. The food was awful."]

result = text_analytics_client.extract_key_phrases(document)

print("Key phrases found:\n")
for phrase in result[0].key_phrases:
    print(phrase)
```


## Detect Language

#### Single text operation

```python
from azure.ai.textanalytics import single_detect_language, TextAnalyticsApiKeyCredential

text = "Redmond is a city in King County, Washington, United States, located 15 miles east of Seattle."

text = "I need to take my cat to the veterinarian."

result = single_detect_language(
    endpoint=endpoint,
    credential=TextAnalyticsApiKeyCredential(key),
    input_text=text,
    country_hint="US"
)

print("Language detected: {}".format(result.primary_language.name))
print("Confidence score: {}\n".format(result.primary_language.score))
```

#### Batch operation passed with single text

```python
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

text_analytics_client = TextAnalyticsClient(endpoint, TextAnalyticsApiKeyCredential(key))

document = ["I need to take my cat to the veterinarian."]

result = text_analytics_client.detect_language(document)

print("Language detected: {}".format(result[0].primary_language.name))
print("Confidence score: {}\n".format(result[0].primary_language.score))
```

