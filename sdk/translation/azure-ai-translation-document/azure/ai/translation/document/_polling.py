# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import logging
try:
    from urlparse import urlparse # type: ignore # pylint: disable=unused-import
except ImportError:
    from urllib.parse import urlparse

from typing import TYPE_CHECKING, TypeVar, Generic
from azure.core.exceptions import AzureError
from azure.core.tracing.decorator import distributed_trace
from azure.core.polling import PollingMethod
from azure.core.polling.base_polling import OperationResourcePolling

if TYPE_CHECKING:
    from typing import Any, Callable, Union, List, Optional, Tuple


PollingReturnType = TypeVar("PollingReturnType")

_LOGGER = logging.getLogger(__name__)

from azure.core.polling.base_polling import (
    LongRunningOperation,
    _is_empty,
    _as_json,
    BadResponse,
    OperationFailed
)

from azure.core.exceptions import HttpResponseError, ODataV4Format

from azure.core.polling.base_polling import (
    LongRunningOperation,
    _is_empty,
    _as_json,
    BadResponse,
    OperationFailed
)

from azure.core.exceptions import HttpResponseError, ODataV4Format


class TranslationPolling(LongRunningOperation):
    """Implements a Location polling.
    """

    def __init__(self):
        self._async_url = None

    def can_poll(self, pipeline_response):
        # type: (PipelineResponseType) -> bool
        """Answer if this polling method could be used.
        """
        response = pipeline_response.http_response
        if not _is_empty(response):
            body = _as_json(response)
            status = body.get("status")
            if status:
                return True
        return False

    def get_polling_url(self):
        # type: () -> str
        """Return the polling URL.
        """
        return self._async_url

    def set_initial_status(self, pipeline_response):
        # type: (PipelineResponseType) -> str
        """Process first response after initiating long running operation.
        :param azure.core.pipeline.PipelineResponse response: initial REST call response.
        """
        self._async_url = pipeline_response.http_response.request.url

        response = pipeline_response.http_response
        if response.status_code in {200, 201, 202, 204} and self._async_url:
            return "InProgress"
        raise OperationFailed("Operation failed or canceled")

    def get_status(self, pipeline_response):
        # type: (PipelineResponseType) -> str
        """Process the latest status update retrieved from a 'location' header.
        :param azure.core.pipeline.PipelineResponse response: latest REST call response.
        :raises: BadResponse if response has no body and not status 202.
        """
        response = pipeline_response.http_response
        if not _is_empty(response):
            body = _as_json(response)
            status = body.get("status")
            if status:
                return self._map_nonstandard_statuses(status, body)
            raise BadResponse("No status found in body")
        raise BadResponse("The response from long running operation does not contain a body.")

    def get_final_get_url(self, pipeline_response):
        # type: (PipelineResponseType) -> Optional[str]
        """If a final GET is needed, returns the URL.
        :rtype: str
        """
        return None

    # pylint: disable=R0201
    def _map_nonstandard_statuses(self, status, body):
        # type: (str, dict) -> str
        """Map non-standard statuses.
        :param str status: lro process status.
        :param str body: pipeline response body.
        """
        # if status == "Running":
        #     return "Succeeded"
        if status == "ValidationFailed":
            self.raise_error(body)
        if status == "Failed":
            # We don't throw in a "Failed" case so this just indicates job completed
            return "Succeeded"
        if status in ["Cancelled", "Cancelling"]:
            return "Canceled"
        return status

    def raise_error(self, body):
        error = body["error"]
        if body["error"].get("innerError", None):
            error = body["error"]["innerError"]
        http_response_error = HttpResponseError(
            message="({}): {}".format(error["code"], error["message"])
        )
        http_response_error.error = ODataV4Format(error)  # set error.code
        raise http_response_error

#
# class TranslationPolling(OperationResourcePolling):
#     """Implements a Location polling.
#     """
#
#     def get_status(self, pipeline_response):
#         # type: (PipelineResponseType) -> str
#         """Process the latest status update retrieved from a 'location' header.
#
#         :param azure.core.pipeline.PipelineResponse response: latest REST call response.
#         :raises: BadResponse if response has no body and not status 202.
#         """
#         response = pipeline_response.http_response
#         if not _is_empty(response):
#             body = _as_json(response)
#             status = body.get("status")
#             if status:
#                 return self._map_nonstandard_statuses(status, body)
#             raise BadResponse("No status found in body")
#         raise BadResponse("The response from long running operation does not contain a body.")
#
#     # pylint: disable=R0201
#     def _map_nonstandard_statuses(self, status, body):
#         # type: (str, dict) -> str
#         """Map non-standard statuses.
#
#         :param str status: lro process status.
#         :param str body: pipeline response body.
#         """
#         if status == "ValidationFailed":
#             self.raise_error(body)
#         if status == "Failed":
#             # We don't throw in a "Failed" case so this just indicates job completed
#             return "Succeeded"
#         if status in ["Cancelled", "Cancelling"]:
#             return "Canceled"
#         return status
#
#     def raise_error(self, body):
#         error = body["error"]
#         if body["error"].get("innerError", None):
#             error = body["error"]["innerError"]
#         http_response_error = HttpResponseError(
#             message="({}): {}".format(error["code"], error["message"])
#         )
#         http_response_error.error = ODataV4Format(error)  # set error.code
#         raise http_response_error
#


class DocumentTranslationPoller(Generic[PollingReturnType]):
    """Poller for long running operations.

    :param client: A pipeline service client
    :type client: ~azure.core.PipelineClient
    :param initial_response: The initial call response
    :type initial_response: ~azure.core.pipeline.PipelineResponse
    :param deserialization_callback: A callback that takes a Response and return a deserialized object.
                                     If a subclass of Model is given, this passes "deserialize" as callback.
    :type deserialization_callback: callable or msrest.serialization.Model
    :param polling_method: The polling strategy to adopt
    :type polling_method: ~azure.core.polling.PollingMethod
    """

    def __init__(self, client, initial_response, deserialization_callback, polling_method):
        # type: (Any, Any, Callable, PollingMethod[PollingReturnType]) -> None
        self._callbacks = []  # type: List[Callable]
        self._polling_method = polling_method

        # This implicit test avoids bringing in an explicit dependency on Model directly
        try:
            deserialization_callback = deserialization_callback.deserialize # type: ignore
        except AttributeError:
            pass

        # Might raise a CloudError
        self._polling_method.initialize(client, initial_response, deserialization_callback)
        self._done = False
        # Prepare thread execution
        # self._thread = None

        # self._exception = None
        # if not self._polling_method.finished():
        #     self._done = threading.Event()
        #     self._thread = threading.Thread(
        #         target=with_current_context(self._start),
        #         name="LROPoller({})".format(uuid.uuid4()))
        #     self._thread.daemon = True
        #     self._thread.start()

    @property
    def job_id(self):
        """Return the job ID for translation

        :rtype: str
        """
        return self._polling_method

    @property
    def details(self):
        """Return the JobStatusResult

        :rtype: JobStatusResult
        """
        pass

    def _start(self):
        """Start the long running operation.
        On completion, runs any callbacks.

        """
        try:
            self._polling_method.run()
        except AzureError as error:
            if not error.continuation_token:
                try:
                    error.continuation_token = self.continuation_token()
                except Exception as err:  # pylint: disable=broad-except
                    _LOGGER.warning("Unable to retrieve continuation token: %s", err)
                    error.continuation_token = None

            self._exception = error
        except Exception as error:  # pylint: disable=broad-except
            self._exception = error

        finally:
            self._done = True

        callbacks, self._callbacks = self._callbacks, []
        while callbacks:
            for call in callbacks:
                call(self._polling_method)
            callbacks, self._callbacks = self._callbacks, []

    def polling_method(self):
        # type: () -> PollingMethod[PollingReturnType]
        """Return the polling method associated to this poller.
        """
        return self._polling_method

    def continuation_token(self):
        # type: () -> str
        """Return a continuation token that allows to restart the poller later.

        :returns: An opaque continuation token
        :rtype: str
        """
        return self._polling_method.get_continuation_token()

    @classmethod
    def from_continuation_token(cls, polling_method, continuation_token, **kwargs):
        # type: (PollingMethod[PollingReturnType], str, Any) -> DocumentTranslationPoller[PollingReturnType]
        client, initial_response, deserialization_callback = polling_method.from_continuation_token(
            continuation_token, **kwargs
        )
        return cls(client, initial_response, deserialization_callback, polling_method)

    def status(self):
        # type: () -> str
        """Returns the current status string.

        :returns: The current status string
        :rtype: str
        """
        self._polling_method.update_status()
        # update the details property
        # might need to use custom polling method
        return self._polling_method.status()

    def result(self, timeout=None):
        # type: (Optional[int]) -> PollingReturnType
        """Return the result of the long running operation, or
        the result available after the specified timeout.

        :returns: The deserialized resource of the long running operation,
         if one is available.
        :raises ~azure.core.exceptions.HttpResponseError: Server problem with the query.
        """
        if timeout:
            self.wait(timeout)
            self._polling_method.update_status()
            return self._polling_method.resource()

        self._start()
        return self._polling_method.resource()

    @distributed_trace
    def wait(self, timeout=None):
        # type: (Optional[int]) -> None
        """Wait on the long running operation for a specified length
        of time. You can check if this call as ended with timeout with the
        "done()" method.

        :param int timeout: Period of time to wait for the long running
         operation to complete (in seconds).
        :raises ~azure.core.exceptions.HttpResponseError: Server problem with the query.
        """

        if timeout is None:
            timeout = self._polling_method._timeout

        self._polling_method._sleep(timeout)
        # try:
        #     # Let's handle possible None in forgiveness here
        #     # https://github.com/python/mypy/issues/8165
        #     raise self._exception # type: ignore
        # except TypeError: # Was None
        #     pass

    def done(self):
        # type: () -> bool
        """Check status of the long running operation.

        :returns: 'True' if the process has completed, else 'False'.
        :rtype: bool
        """
        return self._polling_method.finished()

    def add_done_callback(self, func):
        # type: (Callable) -> None
        """Add callback function to be run once the long running operation
        has completed - regardless of the status of the operation.

        :param callable func: Callback function that takes at least one
         argument, a completed LongRunningOperation.
        """
        # Still use "_done" and not "done", since CBs are executed inside the thread.
        if self._done:
            func(self._polling_method)
        # Let's add them still, for consistency (if you wish to access to it for some reasons)
        self._callbacks.append(func)

    def remove_done_callback(self, func):
        # type: (Callable) -> None
        """Remove a callback from the long running operation.

        :param callable func: The function to be removed from the callbacks.
        :raises ValueError: if the long running operation has already completed.
        """
        if self._done:
            raise ValueError("Process is complete.")
        self._callbacks = [c for c in self._callbacks if c != func]
