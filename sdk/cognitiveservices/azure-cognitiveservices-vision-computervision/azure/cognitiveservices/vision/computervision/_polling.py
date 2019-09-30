# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from azure.core.polling import PollingMethod
import time
import logging
from ._deserialize import deserialize_text_recognition_result

logger = logging.getLogger(__name__)


class ComputerVisionPollingMethod(PollingMethod):

    def __init__(self, interval):
        self._command = None
        self.operation_result = None
        self.operation_status = "NotStarted"
        self.polling_interval = interval

    def _update_status(self):
        result = None
        try:
            result = self._command()
        except Exception as error:
            print(error)
        self.operation_result = result
        self.operation_status = result.status

    def initialize(self, command, initial_status, _):  # pylint: disable=arguments-differ
        self._command = command
        self.operation_status = "NotStarted"

    def run(self):
        try:
            while not self.finished():
                self._update_status()
                time.sleep(self.polling_interval)
        except Exception as e:
            logger.warning(str(e))
            raise

    def status(self):
        self._update_status()
        return self.operation_status

    def finished(self):
        """Is this polling finished?
        :rtype: bool
        """
        return self.operation_status not in ["NotStarted", "Running"]

    def resource(self):
        if not self.finished:
            self._update_status()
        try:
            return deserialize_text_recognition_result(self.operation_result.recognition_result)
        except AttributeError:
            return deserialize_text_recognition_result(self.operation_result.recognition_results)

    # Ask service team if returns a retry-after
    # def _delay(self):
    #     """Check for a 'retry-after' header to set timeout,
    #     otherwise use configured timeout.
    #     """
    #     if self._response is None:
    #         return
    #     if self._response.headers.get('retry-after'):
    #         time.sleep(int(self._response.headers['retry-after']))
    #     else:
    #         time.sleep(self._timeout)