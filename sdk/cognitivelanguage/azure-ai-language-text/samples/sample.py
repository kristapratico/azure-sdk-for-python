from azure.identity import DefaultAzureCredential
from azure.ai.language.text import TextAnalysisClient, AnalyzeSentiment

text_client = TextAnalysisClient("endpoint", DefaultAzureCredential())

result = text_client.analyze_text(kind=AnalyzeSentiment(documents=["I'm tired"], show_opinion_mining=True))

for analyze_sentiment_result in result:
    if analyze_sentiment_result.is_error:
      print("...Is an error with code '{}' and message '{}'".format(
          analyze_sentiment_result.code, analyze_sentiment_result.message
      ))
    else:
        print(f"......Overall sentiment: {analyze_sentiment_result.sentiment}")
        print("......Scores: positive={}; neutral={}; negative={} \n".format(
            analyze_sentiment_result.confidence_scores.positive,
            analyze_sentiment_result.confidence_scores.neutral,
            analyze_sentiment_result.confidence_scores.negative,
        ))