import itertools
from typing import (  # pylint: disable=unused-import
    Callable,
    Optional,
    TypeVar,
    Iterator,
    Iterable,
    Tuple,
)
import logging

from azure.core.exceptions import AzureError


_LOGGER = logging.getLogger(__name__)

ReturnType = TypeVar("ReturnType")
ResponseType = TypeVar("ResponseType")


class DocumentsPageIterator(Iterator[Iterator[ReturnType]]):
    def __init__(
        self,
        get_next,  # type: Callable[[Optional[str]], ResponseType]
        extract_data,  # type: Callable[[ResponseType], Tuple[str, Iterable[ReturnType]]]
        continuation_token=None,  # type: Optional[str]
        **kwargs
    ):
        """Return an iterator of pages.

        :param get_next: Callable that take the continuation token and return a HTTP response
        :param extract_data: Callable that take an HTTP response and return a tuple continuation token,
         list of ReturnType
        :param str continuation_token: The continuation token needed by get_next
        """
        self._get_next = get_next
        self._extract_data = extract_data
        self.continuation_token = continuation_token
        self._did_a_call_already = False
        self._response = None  # type: Optional[ResponseType]
        self._current_page = None  # type: Optional[Iterable[ReturnType]]
        self._transport = kwargs.pop("transport")
        self._polling_interval = kwargs.pop("polling_interval")

    def __iter__(self):
        """Return 'self'."""
        return self

    def __next__(self):
        # type: () -> Iterator[ReturnType]
        if self.continuation_token is None and self._did_a_call_already:
            raise StopIteration("End of paging")
        try:
            if self._did_a_call_already:
                self._extract_delay()
            self._response = self._get_next(self.continuation_token)
        except AzureError as error:
            if not error.continuation_token:
                error.continuation_token = self.continuation_token
            raise

        self._did_a_call_already = True

        self.continuation_token, self._current_page = self._extract_data(self._response)

        return iter(self._current_page)

    def _extract_delay(self):
        retry_after = self._response.http_response.headers.get("Retry-After", None)
        if retry_after:
            self._transport.sleep(int(retry_after))
        else:
            self._transport.sleep(self._polling_interval)

    next = __next__  # Python 2 compatibility.
        # while True:
        #     if self.continuation_token is None and self._did_a_call_already:
        #         raise StopIteration("End of paging")
        #     try:
        #         self._response = self._get_next(self.continuation_token)
        #         completed_docs = []
        #     except AzureError as error:
        #         if not error.continuation_token:
        #             error.continuation_token = self.continuation_token
        #         raise
        #
        #     self._did_a_call_already = True
        #
        #     next_continuation_token, self._current_page = self._extract_data(self._response)
        #
        #     total_doc_count = 0
        #     for doc in self._current_page:
        #         total_doc_count += 1
        #         if doc.id not in completed_docs and doc.status in \
        #                 ["Succeeded", "Failed", "Cancelled", "ValidationFailed"]:
        #             completed_docs.append(doc.id)
        #             yield doc
        #
        #     if len(completed_docs) == total_doc_count:
        #         self.continuation_token = next_continuation_token
        #
        #     if self.continuation_token:
        #         retry_after = self._response.http_response.headers.get("Retry-After", None)
        #         if retry_after:
        #             self._transport.sleep(int(retry_after))
        #         else:
        #             self._transport.sleep(self._polling_interval)


