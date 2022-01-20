# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from typing import TYPE_CHECKING, Union, Any, List, Dict, Optional
from azure.core.tracing.decorator import distributed_trace
from azure.core.paging import ItemPaged
from azure.core.credentials import AzureKeyCredential
from ._models import (
    TextDocumentInput,
    DetectLanguageResult,
    RecognizeEntitiesResult,
    RecognizeLinkedEntitiesResult,
    ExtractKeyPhrasesResult,
    AnalyzeSentimentResult,
    DocumentError,
    RecognizePiiEntitiesResult,
    RecognizeEntitiesAction,
    RecognizePiiEntitiesAction,
    RecognizeLinkedEntitiesAction,
    ExtractKeyPhrasesAction,
    AnalyzeSentimentAction,
    RecognizeEntities,
    RecognizePiiEntities,
    RecognizeLinkedEntities,
    ExtractKeyPhrases,
    AnalyzeSentiment,
    DetectLanguage,
    AnalyzeHealthcareEntitiesAction,
    AnalyzeHealthcareEntitiesResult,
    ExtractSummaryAction,
    ExtractSummaryResult,
    RecognizeCustomEntitiesAction,
    RecognizeCustomEntitiesResult,
    SingleCategoryClassifyAction,
    SingleCategoryClassifyResult,
    MultiCategoryClassifyAction,
    MultiCategoryClassifyResult,
    DetectLanguageInput
)
from ._polling import TextAnalysisLROPoller

if TYPE_CHECKING:
    from azure.core.credentials import TokenCredential


class TextAnalysisClient:
    """Language text analysis.

    :param str endpoint: Supported Language resource
        endpoints (protocol and hostname, for example: https://myresource.cognitiveservices.azure.com).
    :param credential: Credentials needed for the client to connect to Azure.
        This can be the an instance of AzureKeyCredential if using a language API key or a token credential
        from :mod:`azure.identity`.
    :type credential: :class:`~azure.core.credentials.AzureKeyCredential` or
        :class:`~azure.core.credentials.TokenCredential`
    :keyword api_version: The API version of the service to use for requests. It defaults to the
        latest service version. Setting to an older version may result in reduced feature compatibility.
    :paramtype api_version: str

    """

    def __init__(
        self,
        endpoint: str,
        credential: Union[AzureKeyCredential, "TokenCredential"],
        *,
        api_version: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        pass


    @distributed_trace
    def detect_language(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[DetectLanguageInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[DetectLanguageResult, DocumentError]]
        """Detect language for a batch of documents.

        Returns the detected language and a numeric score between zero and
        one. Scores close to one indicate 100% certainty that the identified
        language is true. See https://aka.ms/talangs for the list of enabled languages.

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and country_hint on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.DetectLanguageInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.DetectLanguageInput`, like
            `{"id": "1", "country_hint": "us", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.DetectLanguageInput] or list[dict[str, str]]
        :keyword str country_hint: Country of origin hint for the entire batch. Accepts two
            letter country codes specified by ISO 3166-1 alpha-2. Per-document
            country hints will take precedence over whole batch hints. Defaults to
            "US". If you don't want to use a country hint, pass the string "none".
        :keyword str model_version: Version of the model used on the service side for scoring,
            e.g. "latest", "2019-10-01". If a model version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
            logged on the service side for troubleshooting. By default, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Setting this parameter to true,
            disables input logging and may limit our ability to remediate issues that occur. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.DetectLanguageResult` and
            :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents were
            passed in.
        :rtype: list[~azure.ai.textanalytics.DetectLanguageResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *disable_service_logs* keyword argument.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_detect_language.py
                :start-after: [START detect_language]
                :end-before: [END detect_language]
                :language: python
                :dedent: 4
                :caption: Detecting language in a batch of documents.
        """
        pass

    @distributed_trace
    def recognize_entities(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[RecognizeEntitiesResult, DocumentError]]
        """Recognize entities for a batch of documents.

        Identifies and categorizes entities in your text as people, places,
        organizations, date/time, quantities, percentages, currencies, and more.
        For the list of supported entity types, check: https://aka.ms/taner

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list
            of dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`,
            like `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str language: The 2 letter ISO 639-1 representation of language for the
            entire batch. For example, use "en" for English; "es" for Spanish etc.
            If not set, uses "en" for English as default. Per-document language will
            take precedence over whole batch language. See https://aka.ms/talangs for
            supported languages in Text Analytics API.
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
            logged on the service side for troubleshooting. By default, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Setting this parameter to true,
            disables input logging and may limit our ability to remediate issues that occur. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.RecognizeEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents
            were passed in.
        :rtype: list[~azure.ai.textanalytics.RecognizeEntitiesResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *disable_service_logs* and *string_index_type* keyword arguments.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_recognize_entities.py
                :start-after: [START recognize_entities]
                :end-before: [END recognize_entities]
                :language: python
                :dedent: 4
                :caption: Recognize entities in a batch of documents.
        """
        pass

    @distributed_trace
    def recognize_pii_entities(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[RecognizePiiEntitiesResult, DocumentError]]
        """Recognize entities containing personal information for a batch of documents.

        Returns a list of personal information entities ("SSN",
        "Bank Account", etc) in the document.  For the list of supported entity types,
        check https://aka.ms/tanerpii

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str language: The 2 letter ISO 639-1 representation of language for the
            entire batch. For example, use "en" for English; "es" for Spanish etc.
            If not set, uses "en" for English as default. Per-document language will
            take precedence over whole batch language. See https://aka.ms/talangs for
            supported languages in Text Analytics API.
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword domain_filter: Filters the response entities to ones only included in the specified domain.
            I.e., if set to 'phi', will only return entities in the Protected Healthcare Information domain.
            See https://aka.ms/tanerpii for more information.
        :paramtype domain_filter: str or ~azure.ai.textanalytics.PiiEntityDomain
        :keyword categories_filter: Instead of filtering over all PII entity categories, you can pass in a list of
            the specific PII entity categories you want to filter out. For example, if you only want to filter out
            U.S. social security numbers in a document, you can pass in
            `[PiiEntityCategory.US_SOCIAL_SECURITY_NUMBER]` for this kwarg.
        :paramtype categories_filter: list[str] or list[~azure.ai.textanalytics.PiiEntityCategory]
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.RecognizePiiEntitiesResult`
            and :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents
            were passed in.
        :rtype: list[~azure.ai.textanalytics.RecognizePiiEntitiesResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *recognize_pii_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_recognize_pii_entities.py
                :start-after: [START recognize_pii_entities]
                :end-before: [END recognize_pii_entities]
                :language: python
                :dedent: 4
                :caption: Recognize personally identifiable information entities in a batch of documents.
        """
        pass

    @distributed_trace
    def recognize_linked_entities(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[RecognizeLinkedEntitiesResult, DocumentError]]
        """Recognize linked entities from a well-known knowledge base for a batch of documents.

        Identifies and disambiguates the identity of each entity found in text (for example,
        determining whether an occurrence of the word Mars refers to the planet, or to the
        Roman god of war). Recognized entities are associated with URLs to a well-known
        knowledge base, like Wikipedia.

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str language: The 2 letter ISO 639-1 representation of language for the
            entire batch. For example, use "en" for English; "es" for Spanish etc.
            If not set, uses "en" for English as default. Per-document language will
            take precedence over whole batch language. See https://aka.ms/talangs for
            supported languages in Text Analytics API.
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
            logged on the service side for troubleshooting. By default, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Setting this parameter to true,
            disables input logging and may limit our ability to remediate issues that occur. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.RecognizeLinkedEntitiesResult`
            and :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents
            were passed in.
        :rtype: list[~azure.ai.textanalytics.RecognizeLinkedEntitiesResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *disable_service_logs* and *string_index_type* keyword arguments.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_recognize_linked_entities.py
                :start-after: [START recognize_linked_entities]
                :end-before: [END recognize_linked_entities]
                :language: python
                :dedent: 4
                :caption: Recognize linked entities in a batch of documents.
        """
        pass

    @distributed_trace
    def extract_key_phrases(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[ExtractKeyPhrasesResult, DocumentError]]
        """Extract key phrases from a batch of documents.

        Returns a list of strings denoting the key phrases in the input
        text. For example, for the input text "The food was delicious and there
        were wonderful staff", the API returns the main talking points: "food"
        and "wonderful staff"

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str language: The 2 letter ISO 639-1 representation of language for the
            entire batch. For example, use "en" for English; "es" for Spanish etc.
            If not set, uses "en" for English as default. Per-document language will
            take precedence over whole batch language. See https://aka.ms/talangs for
            supported languages in Text Analytics API.
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
            logged on the service side for troubleshooting. By default, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Setting this parameter to true,
            disables input logging and may limit our ability to remediate issues that occur. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.ExtractKeyPhrasesResult` and
            :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents were
            passed in.
        :rtype: list[~azure.ai.textanalytics.ExtractKeyPhrasesResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *disable_service_logs* keyword argument.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_extract_key_phrases.py
                :start-after: [START extract_key_phrases]
                :end-before: [END extract_key_phrases]
                :language: python
                :dedent: 4
                :caption: Extract the key phrases in a batch of documents.
        """
        pass

    @distributed_trace
    def analyze_sentiment(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):
        # type: (...) -> List[Union[AnalyzeSentimentResult, DocumentError]]
        """Analyze sentiment for a batch of documents. Turn on opinion mining with `show_opinion_mining`.

        Returns a sentiment prediction, as well as sentiment scores for
        each sentiment class (Positive, Negative, and Neutral) for the document
        and each sentence within it.

        See https://docs.microsoft.com/azure/cognitive-services/text-analytics/concepts/data-limits?tabs=version-3
        for document length limits, maximum batch size, and supported text encoding.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of  :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword bool show_opinion_mining: Whether to mine the opinions of a sentence and conduct more
            granular analysis around the aspects of a product or service (also known as
            aspect-based sentiment analysis). If set to true, the returned
            :class:`~azure.ai.textanalytics.SentenceSentiment` objects
            will have property `mined_opinions` containing the result of this analysis. Only available for
            API version v3.1 and up.
        :keyword str language: The 2 letter ISO 639-1 representation of language for the
            entire batch. For example, use "en" for English; "es" for Spanish etc.
            If not set, uses "en" for English as default. Per-document language will
            take precedence over whole batch language. See https://aka.ms/talangs for
            supported languages in Text Analytics API.
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document
            level statistics in the `statistics` field of the document-level response.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword bool disable_service_logs: If set to true, you opt-out of having your text input
            logged on the service side for troubleshooting. By default, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Setting this parameter to true,
            disables input logging and may limit our ability to remediate issues that occur. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: The combined list of :class:`~azure.ai.textanalytics.AnalyzeSentimentResult` and
            :class:`~azure.ai.textanalytics.DocumentError` in the order the original documents were
            passed in.
        :rtype: list[~azure.ai.textanalytics.AnalyzeSentimentResult or ~azure.ai.textanalytics.DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError:

        .. versionadded:: v3.1
            The *show_opinion_mining*, *disable_service_logs*, and *string_index_type* keyword arguments.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_sentiment.py
                :start-after: [START analyze_sentiment]
                :end-before: [END analyze_sentiment]
                :language: python
                :dedent: 4
                :caption: Analyze sentiment in a batch of documents.
        """
        pass


    @distributed_trace
    def begin_analyze_healthcare_entities(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):  # type: (...) -> TextAnalysisLROPoller[ItemPaged[Union[AnalyzeHealthcareEntitiesResult, DocumentError]]]  # pylint: disable=line-too-long
        """Analyze healthcare entities and identify relationships between these entities in a batch of documents.

        Entities are associated with references that can be found in existing knowledge bases,
        such as UMLS, CHV, MSH, etc.

        We also extract the relations found between entities, for example in "The subject took 100 mg of ibuprofen",
        we would extract the relationship between the "100 mg" dosage and the "ibuprofen" medication.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword int polling_interval: Waiting time between two polls for LRO operations
            if no Retry-After header is present. Defaults to 5 seconds.
        :keyword str continuation_token:
            Call `continuation_token()` on the poller object to save the long-running operation (LRO)
            state into an opaque token. Pass the value as the `continuation_token` keyword argument
            to restart the LRO from a saved state.
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: An instance of an TextAnalysisLROPoller. Call `result()` on the this
            object to return a heterogeneous pageable of
            :class:`~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError`.
        :rtype:
            ~azure.ai.textanalytics.TextAnalysisLROPoller[~azure.core.paging.ItemPaged[
            ~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult or ~azure.ai.textanalytics.DocumentError]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:

        .. versionadded:: v3.1
            The *begin_analyze_healthcare_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_healthcare_entities.py
                :start-after: [START analyze_healthcare_entities]
                :end-before: [END analyze_healthcare_entities]
                :language: python
                :dedent: 4
                :caption: Recognize healthcare entities in a batch of documents.
        """
        pass

    @distributed_trace
    def begin_extract_summary(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):  # type: (...) -> TextAnalysisLROPoller[ItemPaged[Union[ExtractSummaryResult, DocumentError]]]  # pylint: disable=line-too-long
        """Analyze healthcare entities and identify relationships between these entities in a batch of documents.

        Entities are associated with references that can be found in existing knowledge bases,
        such as UMLS, CHV, MSH, etc.

        We also extract the relations found between entities, for example in "The subject took 100 mg of ibuprofen",
        we would extract the relationship between the "100 mg" dosage and the "ibuprofen" medication.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword int polling_interval: Waiting time between two polls for LRO operations
            if no Retry-After header is present. Defaults to 5 seconds.
        :keyword str continuation_token:
            Call `continuation_token()` on the poller object to save the long-running operation (LRO)
            state into an opaque token. Pass the value as the `continuation_token` keyword argument
            to restart the LRO from a saved state.
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: An instance of an TextAnalysisLROPoller. Call `result()` on the this
            object to return a heterogeneous pageable of
            :class:`~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError`.
        :rtype:
            ~azure.ai.textanalytics.TextAnalysisLROPoller[~azure.core.paging.ItemPaged[
            ~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult or ~azure.ai.textanalytics.DocumentError]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:

        .. versionadded:: v3.1
            The *begin_analyze_healthcare_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_healthcare_entities.py
                :start-after: [START analyze_healthcare_entities]
                :end-before: [END analyze_healthcare_entities]
                :language: python
                :dedent: 4
                :caption: Recognize healthcare entities in a batch of documents.
        """
        pass


    @distributed_trace
    def begin_recognize_custom_entities(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):  # type: (...) -> TextAnalysisLROPoller[ItemPaged[Union[RecognizeCustomEntitiesResult, DocumentError]]]  # pylint: disable=line-too-long
        """Analyze healthcare entities and identify relationships between these entities in a batch of documents.

        Entities are associated with references that can be found in existing knowledge bases,
        such as UMLS, CHV, MSH, etc.

        We also extract the relations found between entities, for example in "The subject took 100 mg of ibuprofen",
        we would extract the relationship between the "100 mg" dosage and the "ibuprofen" medication.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword int polling_interval: Waiting time between two polls for LRO operations
            if no Retry-After header is present. Defaults to 5 seconds.
        :keyword str continuation_token:
            Call `continuation_token()` on the poller object to save the long-running operation (LRO)
            state into an opaque token. Pass the value as the `continuation_token` keyword argument
            to restart the LRO from a saved state.
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: An instance of an TextAnalysisLROPoller. Call `result()` on the this
            object to return a heterogeneous pageable of
            :class:`~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError`.
        :rtype:
            ~azure.ai.textanalytics.TextAnalysisLROPoller[~azure.core.paging.ItemPaged[
            ~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult or ~azure.ai.textanalytics.DocumentError]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:

        .. versionadded:: v3.1
            The *begin_analyze_healthcare_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_healthcare_entities.py
                :start-after: [START analyze_healthcare_entities]
                :end-before: [END analyze_healthcare_entities]
                :language: python
                :dedent: 4
                :caption: Recognize healthcare entities in a batch of documents.
        """
        pass


    @distributed_trace
    def begin_single_category_classify(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):  # type: (...) -> TextAnalysisLROPoller[ItemPaged[Union[SingleCategoryClassifyResult, DocumentError]]]  # pylint: disable=line-too-long
        """Analyze healthcare entities and identify relationships between these entities in a batch of documents.

        Entities are associated with references that can be found in existing knowledge bases,
        such as UMLS, CHV, MSH, etc.

        We also extract the relations found between entities, for example in "The subject took 100 mg of ibuprofen",
        we would extract the relationship between the "100 mg" dosage and the "ibuprofen" medication.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword int polling_interval: Waiting time between two polls for LRO operations
            if no Retry-After header is present. Defaults to 5 seconds.
        :keyword str continuation_token:
            Call `continuation_token()` on the poller object to save the long-running operation (LRO)
            state into an opaque token. Pass the value as the `continuation_token` keyword argument
            to restart the LRO from a saved state.
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: An instance of an TextAnalysisLROPoller. Call `result()` on the this
            object to return a heterogeneous pageable of
            :class:`~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError`.
        :rtype:
            ~azure.ai.textanalytics.TextAnalysisLROPoller[~azure.core.paging.ItemPaged[
            ~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult or ~azure.ai.textanalytics.DocumentError]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:

        .. versionadded:: v3.1
            The *begin_analyze_healthcare_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_healthcare_entities.py
                :start-after: [START analyze_healthcare_entities]
                :end-before: [END analyze_healthcare_entities]
                :language: python
                :dedent: 4
                :caption: Recognize healthcare entities in a batch of documents.
        """
        pass

    @distributed_trace
    def begin_multi_category_classify(  # type: ignore
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        **kwargs  # type: Any
    ):  # type: (...) -> TextAnalysisLROPoller[ItemPaged[Union[MultiCategoryClassifyResult, DocumentError]]]  # pylint: disable=line-too-long
        """Analyze healthcare entities and identify relationships between these entities in a batch of documents.

        Entities are associated with references that can be found in existing knowledge bases,
        such as UMLS, CHV, MSH, etc.

        We also extract the relations found between entities, for example in "The subject took 100 mg of ibuprofen",
        we would extract the relationship between the "100 mg" dosage and the "ibuprofen" medication.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents:
            list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or
            list[dict[str, str]]
        :keyword str model_version: This value indicates which model will
            be used for scoring, e.g. "latest", "2019-10-01". If a model-version
            is not specified, the API will default to the latest, non-preview version.
            See here for more info: https://aka.ms/text-analytics-model-versioning
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :keyword str string_index_type: Specifies the method used to interpret string offsets.
            `UnicodeCodePoint`, the Python encoding, is the default. To override the Python default,
            you can also pass in `Utf16CodePoint` or `TextElement_v8`. For additional information
            see https://aka.ms/text-analytics-offsets
        :keyword int polling_interval: Waiting time between two polls for LRO operations
            if no Retry-After header is present. Defaults to 5 seconds.
        :keyword str continuation_token:
            Call `continuation_token()` on the poller object to save the long-running operation (LRO)
            state into an opaque token. Pass the value as the `continuation_token` keyword argument
            to restart the LRO from a saved state.
        :keyword bool disable_service_logs: Defaults to true, meaning that Text Analytics will not log your
            input text on the service side for troubleshooting. If set to False, Text Analytics logs your
            input text for 48 hours, solely to allow for troubleshooting issues in providing you with
            the Text Analytics natural language processing functions. Please see
            Cognitive Services Compliance and Privacy notes at https://aka.ms/cs-compliance for
            additional details, and Microsoft Responsible AI principles at
            https://www.microsoft.com/ai/responsible-ai.
        :return: An instance of an TextAnalysisLROPoller. Call `result()` on the this
            object to return a heterogeneous pageable of
            :class:`~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult` and
            :class:`~azure.ai.textanalytics.DocumentError`.
        :rtype:
            ~azure.ai.textanalytics.TextAnalysisLROPoller[~azure.core.paging.ItemPaged[
            ~azure.ai.textanalytics.AnalyzeHealthcareEntitiesResult or ~azure.ai.textanalytics.DocumentError]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:

        .. versionadded:: v3.1
            The *begin_analyze_healthcare_entities* client method.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sample_analyze_healthcare_entities.py
                :start-after: [START analyze_healthcare_entities]
                :end-before: [END analyze_healthcare_entities]
                :language: python
                :dedent: 4
                :caption: Recognize healthcare entities in a batch of documents.
        """
        pass


    # @distributed_trace
    # def analyze_text(
    #     self,
    #     kind: Union[
    #         RecognizeEntities,
    #         RecognizeLinkedEntities,
    #         RecognizePiiEntities,
    #         ExtractKeyPhrases,
    #         AnalyzeSentiment,
    #         DetectLanguage,
    #     ],
    #     **kwargs: Any
    # ) -> List[Union[
    #         RecognizeEntitiesResult,
    #         RecognizeLinkedEntitiesResult,
    #         RecognizePiiEntitiesResult,
    #         ExtractKeyPhrasesResult,
    #         AnalyzeSentimentResult,
    #         DetectLanguageResult,
    #         DocumentError,
    #     ]
    # ]:
    #     """analyze text.
    # 
    #     :param kind: Analysis kind.
    #     :type kind: RecognizeEntities or RecognizePiiEntities or ExtractKeyPhrases or
    #      RecognizeLinkedEntities or AnalyzeSentiment or DetectLanguage
    #     :keyword str api_version:
    #     :keyword bool show_stats: If set to true, response will contain document level statistics.
    #     :return: A list of the type of the action specified.
    #     :rtype: list[RecognizeEntitiesResult or RecognizeLinkedEntitiesResult or RecognizePiiEntitiesResult,
    #      ExtractKeyPhrasesResult or AnalyzeSentimentResult or DetectLanguageResult or DocumentError]
    #     :raises: ~azure.core.exceptions.HttpResponseError
    #     """
    #     pass

    # @distributed_trace
    # def analyze_text_2(
    #     self,
    #     documents: Union[List[str], Union[List[TextDocumentInput], List[DetectLanguageInput]], List[Dict[str, str]]],
    #     kind: Union[
    #         RecognizeEntitiesAction,
    #         RecognizeLinkedEntitiesAction,
    #         RecognizePiiEntitiesAction,
    #         ExtractKeyPhrasesAction,
    #         AnalyzeSentimentAction,
    #         DetectLanguageAction,
    #     ],
    #     **kwargs: Any
    # ) -> List[
    #     Union[
    #         RecognizeEntitiesResult,
    #         RecognizeLinkedEntitiesResult,
    #         RecognizePiiEntitiesResult,
    #         ExtractKeyPhrasesResult,
    #         AnalyzeSentimentResult,
    #         DetectLanguageResult,
    #         DocumentError,
    #     ]
    # ]:
    #     pass

    # @distributed_trace
    # def begin_analyze_actions(
    #     self,
    #     documents: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]],
    #     actions: List[
    #         Union[
    #             RecognizeEntitiesAction,
    #             RecognizeLinkedEntitiesAction,
    #             RecognizePiiEntitiesAction,
    #             ExtractKeyPhrasesAction,
    #             AnalyzeSentimentAction,
    #             ExtractSummaryAction,
    #             RecognizeCustomEntitiesAction,
    #             SingleCategoryClassifyAction,
    #             MultiCategoryClassifyAction,
    #             AnalyzeHealthcareEntitiesAction,
    #         ]
    #     ],
    #     **kwargs: Any
    # ) -> TextAnalysisLROPoller[
    #     ItemPaged[
    #         List[
    #             Union[
    #                 RecognizeEntitiesResult,
    #                 RecognizeLinkedEntitiesResult,
    #                 RecognizePiiEntitiesResult,
    #                 ExtractKeyPhrasesResult,
    #                 AnalyzeSentimentResult,
    #                 ExtractSummaryResult,
    #                 RecognizeCustomEntitiesResult,
    #                 SingleCategoryClassifyResult,
    #                 MultiCategoryClassifyResult,
    #                 AnalyzeHealthcareEntitiesResult,
    #                 DocumentError,
    #             ]
    #         ]
    #     ]
    # ]:
    #     """Begin analyze actions.
    #
    #     :param documents: The set of documents to process as part of this batch.
    #         If you wish to specify the ID and language on a per-item basis you must
    #         use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
    #         dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
    #         `{"id": "1", "language": "en", "text": "hello world"}`.
    #     :type documents: list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
    #     :param actions: A heterogeneous list of actions to perform on the input documents.
    #         Each action object encapsulates the parameters used for the particular action type.
    #         The action results will be in the same order of the input actions.
    #     :type actions: list[RecognizeEntitiesAction or RecognizePiiEntitiesAction or ExtractKeyPhrasesAction or
    #      RecognizeLinkedEntitiesAction or AnalyzeSentimentAction or ExtractSummaryAction or
    #      or RecognizeCustomEntitiesAction or SingleCategoryClassifyAction or MultiCategoryClassifyAction or
    #      AnalyzeHealthcareEntitiesAction]
    #     :keyword str api_version:
    #     :keyword str display_name: An optional display name to set for the requested analysis.
    #     :keyword bool show_stats: If set to true, response will contain document level statistics.
    #     :return: An instance of an TextAnalysisLROPoller. Call `result()` on the poller
    #         object to return a pageable heterogeneous list of lists. This list of lists is first ordered
    #         by the documents you input, then ordered by the actions you input. For example,
    #         if you have documents input ["Hello", "world"], and actions
    #         :class:`~azure.ai.textanalytics.RecognizeEntitiesAction` and
    #         :class:`~azure.ai.textanalytics.AnalyzeSentimentAction`, when iterating over the list of lists,
    #         you will first iterate over the action results for the "Hello" document, getting the
    #         :class:`~azure.ai.textanalytics.RecognizeEntitiesResult` of "Hello",
    #         then the :class:`~azure.ai.textanalytics.AnalyzeSentimentResult` of "Hello".
    #         Then, you will get the :class:`~azure.ai.textanalytics.RecognizeEntitiesResult` and
    #         :class:`~azure.ai.textanalytics.AnalyzeSentimentResult` of "world".
    #     :rtype: TextAnalysisLROPoller[ItemPaged[list[RecognizeEntitiesResult or RecognizeLinkedEntitiesResult or
    #      RecognizePiiEntitiesResult or ExtractKeyPhrasesResult or AnalyzeSentimentResult or ExtractSummaryAction or
    #      RecognizeCustomEntitiesResult or SingleCategoryClassifyResult or MultiCategoryClassifyResult or
    #      AnalyzeHealthcareEntitiesResult or DocumentError]]]
    #     :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:
    #     """
    #
    #     pass
