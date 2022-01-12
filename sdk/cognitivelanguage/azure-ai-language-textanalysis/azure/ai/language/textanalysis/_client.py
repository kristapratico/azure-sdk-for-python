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
    DetectLanguageAction,
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
)
from ._polling import AnalyzeActionsLROPoller

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
        api_version: str = None,
        **kwargs: Any
    ) -> None:
        pass

    @distributed_trace
    def analyze_text(
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        action,  # type: Union[RecognizeEntitiesAction, RecognizeLinkedEntitiesAction, RecognizePiiEntitiesAction, ExtractKeyPhrasesAction, AnalyzeSentimentAction, ExtractSummaryAction, RecognizeCustomEntitiesAction, SingleCategoryClassifyAction, MultiCategoryClassifyAction, AnalyzeHealthcareEntitiesAction] # pylint: disable=line-too-long
        **kwargs  # type: Any
    ):  # type: (...) -> List[Union[RecognizeEntitiesResult, RecognizeLinkedEntitiesResult, RecognizePiiEntitiesResult, ExtractKeyPhrasesResult, AnalyzeSentimentResult, ExtractSummaryResult, RecognizeCustomEntitiesResult, SingleCategoryClassifyResult, MultiCategoryClassifyResult, AnalyzeHealthcareEntitiesResult, DocumentError]]  # pylint: disable=line-too-long
        """analyze text.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents: list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :param action: A heterogeneous list of actions to perform on the input documents.
            Each action object encapsulates the parameters used for the particular action type.
            The action results will be in the same order of the input actions.
        :type action: RecognizeEntitiesAction or RecognizePiiEntitiesAction or ExtractKeyPhrasesAction or RecognizeLinkedEntitiesAction or AnalyzeSentimentAction or ExtractSummaryAction or RecognizeCustomEntitiesAction or SingleCategoryClassifyAction or MultiCategoryClassifyAction or AnalyzeHealthcareEntitiesAction
        :keyword str api_version:
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :return: A list of the type of the action specified.
        :rtype: list[RecognizeEntitiesResult or RecognizeLinkedEntitiesResult or RecognizePiiEntitiesResult, ExtractKeyPhrasesResult or AnalyzeSentimentResult or ExtractSummaryAction or RecognizeCustomEntitiesResult or SingleCategoryClassifyResult or MultiCategoryClassifyResult or AnalyzeHealthcareEntitiesResult or DocumentError]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:
        """
        pass

    @distributed_trace
    def begin_analyze_actions(
        self,
        documents,  # type: Union[List[str], List[TextDocumentInput], List[Dict[str, str]]]
        actions,  # type: List[Union[RecognizeEntitiesAction, RecognizeLinkedEntitiesAction, RecognizePiiEntitiesAction, ExtractKeyPhrasesAction, AnalyzeSentimentAction, ExtractSummaryAction, RecognizeCustomEntitiesAction, SingleCategoryClassifyAction, MultiCategoryClassifyAction, AnalyzeHealthcareEntitiesAction]] # pylint: disable=line-too-long
        **kwargs  # type: Any
    ):  # type: (...) -> AnalyzeActionsLROPoller[ItemPaged[List[Union[RecognizeEntitiesResult, RecognizeLinkedEntitiesResult, RecognizePiiEntitiesResult, ExtractKeyPhrasesResult, AnalyzeSentimentResult, ExtractSummaryResult, RecognizeCustomEntitiesResult, SingleCategoryClassifyResult, MultiCategoryClassifyResult, AnalyzeHealthcareEntitiesResult, DocumentError]]]]  # pylint: disable=line-too-long
        """Begin analyze actions.

        :param documents: The set of documents to process as part of this batch.
            If you wish to specify the ID and language on a per-item basis you must
            use as input a list[:class:`~azure.ai.textanalytics.TextDocumentInput`] or a list of
            dict representations of :class:`~azure.ai.textanalytics.TextDocumentInput`, like
            `{"id": "1", "language": "en", "text": "hello world"}`.
        :type documents: list[str] or list[~azure.ai.textanalytics.TextDocumentInput] or list[dict[str, str]]
        :param actions: A heterogeneous list of actions to perform on the input documents.
            Each action object encapsulates the parameters used for the particular action type.
            The action results will be in the same order of the input actions.
        :type actions: list[RecognizeEntitiesAction or RecognizePiiEntitiesAction or ExtractKeyPhrasesAction or RecognizeLinkedEntitiesAction or AnalyzeSentimentAction or ExtractSummaryAction or RecognizeCustomEntitiesAction or SingleCategoryClassifyAction or MultiCategoryClassifyAction or AnalyzeHealthcareEntitiesAction]
        :keyword str api_version:
        :keyword str display_name: An optional display name to set for the requested analysis.
        :keyword bool show_stats: If set to true, response will contain document level statistics.
        :return: An instance of an AnalyzeActionsLROPoller. Call `result()` on the poller
            object to return a pageable heterogeneous list of lists. This list of lists is first ordered
            by the documents you input, then ordered by the actions you input. For example,
            if you have documents input ["Hello", "world"], and actions
            :class:`~azure.ai.textanalytics.RecognizeEntitiesAction` and
            :class:`~azure.ai.textanalytics.AnalyzeSentimentAction`, when iterating over the list of lists,
            you will first iterate over the action results for the "Hello" document, getting the
            :class:`~azure.ai.textanalytics.RecognizeEntitiesResult` of "Hello",
            then the :class:`~azure.ai.textanalytics.AnalyzeSentimentResult` of "Hello".
            Then, you will get the :class:`~azure.ai.textanalytics.RecognizeEntitiesResult` and
            :class:`~azure.ai.textanalytics.AnalyzeSentimentResult` of "world".
        :rtype: AnalyzeActionsLROPoller[ItemPaged[list[RecognizeEntitiesResult or RecognizeLinkedEntitiesResult or RecognizePiiEntitiesResult or ExtractKeyPhrasesResult or AnalyzeSentimentResult or ExtractSummaryAction or RecognizeCustomEntitiesResult or SingleCategoryClassifyResult or MultiCategoryClassifyResult or AnalyzeHealthcareEntitiesResult or DocumentError]]]
        :raises ~azure.core.exceptions.HttpResponseError or TypeError or ValueError or NotImplementedError:
        """

        pass
