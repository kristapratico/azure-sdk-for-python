# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
from azure.core.polling import LROPoller
from azure.cognitiveservices.vision.computervision._generated._computer_vision_client import ComputerVision
from azure.cognitiveservices.vision.computervision._generated.models import ComputerVisionErrorException
from azure.cognitiveservices.vision.computervision._polling import ComputerVisionPollingMethod

def response_handler(response, deserialized, response_headers):
    return response


class ComputerVisionClient(ComputerVision):

    def __init__(self, endpoint, credentials, **kwargs):
        super(ComputerVisionClient, self).__init__(endpoint=endpoint, credentials=credentials, **kwargs)

    def analyze_image(self, url, visual_features=None, details=None, language="en", description_exclude=None, **kwargs):
        try:
            return self.vision.analyze_image(
                url=url,
                visual_features=visual_features,
                details=details,
                language=language,
                description_exclude=description_exclude,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def describe_image(self, url, max_candidates=1, language="en", description_exclude=None, **kwargs):
        try:
            return self.vision.describe_image(
                url=url,
                max_candidates=max_candidates,
                language=language,
                description_exclude=description_exclude,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def detect_objects(self, url, **kwargs):
        try:
            return self.vision.detect_objects(
                url=url,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def list_models(self, **kwargs):
        try:
            self.vision.list_models(
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def analyze_image_by_domain(self, model, url, language="en", **kwargs):
        try:
            return self.vision.analyze_image_by_domain(
                model=model,
                url=url,
                langauge=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def recognize_printed_text(self, url, detect_orientation=True, language="unk", **kwargs):
        try:
            return self.vision.recognize_printed_text(
                url=url,
                detect_orientation=detect_orientation,
                langauge=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def tag_image(self, url, language="en", **kwargs):
        try:
            return self.vision.tag_image(
                url=url,
                langauge=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def generate_thumbnail(self, width, height, url, smart_cropping=False, **kwargs):
        try:
            return self.vision.generate_thumbnail(
                width=width,
                height=height,
                url=url,
                smart_cropping=smart_cropping,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def get_area_of_interest(self, url, **kwargs):
        try:
            return self.vision.get_area_of_interest(
                url=url,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def analyze_image_in_stream(
        self, image,
        visual_features=None,
        details=None,
        language="en",
        description_exclude=None,
        **kwargs
    ):
        try:
            return self.vision.analyze_image_in_stream(
                image=image,
                visual_features=visual_features,
                details=details,
                language=language,
                description_exclude=description_exclude,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def get_area_of_interest_in_stream(self, image, **kwargs):
        try:
            return self.vision.get_area_of_interest_in_stream(
                image=image,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def describe_image_in_stream(self, image, max_candidates=1, language="en", description_exclude=None, **kwargs):
        try:
            return self.vision.describe_image_in_stream(
                image=image,
                max_candidates=max_candidates,
                language=language,
                description_exclude=description_exclude,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def detect_objects_in_stream(self, image, **kwargs):
        try:
            return self.vision.detect_objects_in_stream(
                image=image,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def generate_thumbnail_in_stream(self, width, height, image, smart_cropping=False, **kwargs):
        try:
            return self.vision.generate_thumbnail_in_stream(
                width=width,
                height=height,
                image=image,
                smart_cropping=smart_cropping,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def analyze_image_by_domain_in_stream(self, model, image, language="en", **kwargs):
        try:
            return self.vision.analyze_image_by_domain_in_stream(
                model=model,
                image=image,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def recognize_printed_text_in_stream(self, image, detect_orientation=True, language="unk", **kwargs):
        try:
            return self.vision.recognize_printed_text_in_stream(
                image=image,
                detect_orientation=detect_orientation,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def tag_image_in_stream(self, image, language="en", **kwargs):
        try:
            return self.vision.tag_image_in_stream(
                image=image,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def recognize_text(self, mode, url, **kwargs):
        try:
            job = self.vision.recognize_text(
                mode=mode,
                url=url,
                cls=response_handler,
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self.vision.get_text_operation_result,
            operation_id,
        )

        try:
            start_recognize_text = command()
        except ComputerVisionErrorException as error:
            raise error
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_recognize_text, None, polling_method)

    def batch_read_file(self, url, **kwargs):
        try:
            job = self.vision.batch_read_file(
                url=url,
                cls=response_handler,
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self.vision.get_read_operation_result,
            operation_id,
        )

        try:
            start_batch_read_file = command()
        except ComputerVisionErrorException as error:
            raise error
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_batch_read_file, None, polling_method)

    def recognize_text_in_stream(self, image, mode, **kwargs):
        try:
            job = self.vision.recognize_text_in_stream(
                image=image,
                mode=mode,
                cls=response_handler,
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self.vision.get_text_operation_result,
            operation_id,
        )

        try:
            start_recognize_text_in_stream = command()
        except ComputerVisionErrorException as error:
            raise error
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_recognize_text_in_stream, None, polling_method)

    def batch_read_file_in_stream(self, image, **kwargs):
        try:
            job = self.vision.batch_read_file_in_stream(
                image=image,
                cls=response_handler,
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self.vision.get_read_operation_result,
            operation_id,
        )

        try:
            start_batch_read_file_in_stream = command()
        except ComputerVisionErrorException as error:
            raise error
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_batch_read_file_in_stream, None, polling_method)