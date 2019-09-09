# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
import six
import io
from azure.core.polling import LROPoller
from azure.cognitiveservices.vision.computervision._generated._computer_vision_client import ComputerVision
from azure.cognitiveservices.vision.computervision._generated.models import ComputerVisionErrorException
from azure.cognitiveservices.vision.computervision._polling import ComputerVisionPollingMethod

def response_handler(response, deserialized, response_headers):
    return response


class ComputerVisionClient(ComputerVision):
    """The Computer Vision API provides state-of-the-art algorithms to process images and return information.
    For example, it can be used to determine if an image contains mature content, or it can be used to find all the
    faces in an image.  It also has other features like estimating dominant and accent colors, categorizing the content
    of images, and describing an image with complete English sentences.  Additionally, it can also intelligently
    generate images thumbnails for displaying large images effectively.

    :param endpoint: Supported Cognitive Services endpoints.
    :type endpoint: str
    :param credentials: Cognitive Services account key credentials needed for the client to connect to Azure.
    :type credentials: str
    """
    def __init__(self, endpoint, credentials, **kwargs):
        super(ComputerVisionClient, self).__init__(endpoint=endpoint, credentials=credentials, **kwargs)

    def analyze_image(self, data, visual_features=None, details=None, language="en", description_exclude=None, **kwargs):
        """This operation extracts a rich set of visual features based on the
        image content.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL. Within your request, there is an optional
        parameter to allow you to choose which features to return. By default,
        image categories are returned in the response.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param visual_features: A string indicating what visual feature types
         to return. Multiple values should be comma-separated. Valid visual
         feature types include: Categories - categorizes image content
         according to a taxonomy defined in documentation. Tags - tags the
         image with a detailed list of words related to the image content.
         Description - describes the image content with a complete English
         sentence. Faces - detects if faces are present. If present, generate
         coordinates, gender and age. ImageType - detects if image is clipart
         or a line drawing. Color - determines the accent color, dominant
         color, and whether an image is black&white. Adult - detects if the
         image is pornographic in nature (depicts nudity or a sex act), or is
         gory (depicts extreme violence or blood). Sexually suggestive content
         (aka racy content) is also detected. Objects - detects various objects
         within an image, including the approximate location. The Objects
         argument is only available in English. Brands - detects various brands
         within an image, including the approximate location. The Brands
         argument is only available in English.
        :type visual_features: list[str or
         ~computervision.models.VisualFeatureTypes]
        :param details: A string indicating which domain-specific details to
         return. Multiple values should be comma-separated. Valid visual
         feature types include: Celebrities - identifies celebrities if
         detected in the image, Landmarks - identifies notable landmarks in the
         image.
        :type details: list[str or ~computervision.models.Details]
        :param language: The desired language for output generation. If this
         parameter is not specified, the default value is
         &quot;en&quot;.Supported languages:en - English, Default. es -
         Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.
         Possible values include: 'en', 'es', 'ja', 'pt', 'zh'
        :type language: str
        :param description_exclude: Turn off specified domain models when
         generating the description.
        :type description_exclude: list[str or
         ~computervision.models.DescriptionExclude]
        :return: ImageAnalysis
        :rtype: ~computervision.models.ImageAnalysis
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        if isinstance(data, six.text_type):
            try:
                return self.vision.analyze_image(
                    url=data,
                    visual_features=visual_features,
                    details=details,
                    language=language,
                    description_exclude=description_exclude,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            except ComputerVisionErrorException as error:
                raise error
        if isinstance(data, io.BufferedReader):
            try:
                return self.vision.analyze_image_in_stream(
                    image=data,
                    visual_features=visual_features,
                    details=details,
                    language=language,
                    description_exclude=description_exclude,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported data type: {}".format(type(data)))

    def describe_image(self, url, max_candidates=1, language="en", description_exclude=None, **kwargs):
        """This operation generates a description of an image in human readable
        language with complete sentences. The description is based on a
        collection of content tags, which are also returned by the operation.
        More than one description can be generated for each image. Descriptions
        are ordered by their confidence score. Descriptions may include results
        from celebrity and landmark domain models, if applicable.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param max_candidates: Maximum number of candidate descriptions to be
         returned.  The default is 1.
        :type max_candidates: int
        :param language: The desired language for output generation. If this
         parameter is not specified, the default value is
         &quot;en&quot;.Supported languages:en - English, Default. es -
         Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.
         Possible values include: 'en', 'es', 'ja', 'pt', 'zh'
        :type language: str
        :param description_exclude: Turn off specified domain models when
         generating the description.
        :type description_exclude: list[str or
         ~computervision.models.DescriptionExclude]
        :return: ImageDescription
        :rtype: ~computervision.models.ImageDescription
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
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
        """Performs object detection on the specified image.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :return: DetectResult
        :rtype: ~computervision.models.DetectResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            return self.vision.detect_objects(
                url=url,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def list_models(self, **kwargs):
        """This operation returns the list of domain-specific models that are
        supported by the Computer Vision API. Currently, the API supports
        following domain-specific models: celebrity recognizer, landmark
        recognizer.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :return: ListModelsResult
        :rtype: ~computervision.models.ListModelsResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            return self.vision.list_models(
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def analyze_image_by_domain(self, model, url, language="en", **kwargs):
        """This operation recognizes content within an image by applying a
        domain-specific model. The list of domain-specific models that are
        supported by the Computer Vision API can be retrieved using the /models
        GET request. Currently, the API provides following domain-specific
        models: celebrities, landmarks.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL.
        A successful response will be returned in JSON.
        If the request failed, the response will contain an error code and a
        message to help understand what went wrong.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param model: The domain-specific content to recognize.
        :type model: str
        :param language: The desired language for output generation. If this
         parameter is not specified, the default value is
         &quot;en&quot;.Supported languages:en - English, Default. es -
         Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.
         Possible values include: 'en', 'es', 'ja', 'pt', 'zh'
        :type language: str
        :return: DomainModelResults
        :rtype: ~computervision.models.DomainModelResults
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            return self.vision.analyze_image_by_domain(
                model=model,
                url=url,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def recognize_printed_text(self, url, detect_orientation=True, language="unk", **kwargs):
        """Optical Character Recognition (OCR) detects text in an image and
        extracts the recognized characters into a machine-usable character
        stream.
        Upon success, the OCR results will be returned.
        Upon failure, the error code together with an error message will be
        returned. The error code can be one of InvalidImageUrl,
        InvalidImageFormat, InvalidImageSize, NotSupportedImage,
        NotSupportedLanguage, or InternalServerError.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param detect_orientation: Whether detect the text orientation in the
         image. With detectOrientation=true the OCR service tries to detect the
         image orientation and correct it before further processing (e.g. if
         it's upside-down).
        :type detect_orientation: bool
        :param language: The BCP-47 language code of the text to be detected
         in the image. The default value is 'unk'. Possible values include:
         'unk', 'zh-Hans', 'zh-Hant', 'cs', 'da', 'nl', 'en', 'fi', 'fr', 'de',
         'el', 'hu', 'it', 'ja', 'ko', 'nb', 'pl', 'pt', 'ru', 'es', 'sv',
         'tr', 'ar', 'ro', 'sr-Cyrl', 'sr-Latn', 'sk'
        :type language: str or ~computervision.models.OcrLanguages
        :return: OcrResult
        :rtype: ~computervision.models.OcrResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            return self.vision.recognize_printed_text(
                url=url,
                detect_orientation=detect_orientation,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def tag_image(self, url, language="en", **kwargs):
        """This operation generates a list of words, or tags, that are relevant to
        the content of the supplied image. The Computer Vision API can return
        tags based on objects, living beings, scenery or actions found in
        images. Unlike categories, tags are not organized according to a
        hierarchical classification system, but correspond to image content.
        Tags may contain hints to avoid ambiguity or provide context, for
        example the tag "ascomycete" may be accompanied by the hint "fungus".
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param language: The desired language for output generation. If this
         parameter is not specified, the default value is
         &quot;en&quot;.Supported languages:en - English, Default. es -
         Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.
         Possible values include: 'en', 'es', 'ja', 'pt', 'zh'
        :type language: str
        :return: TagResult
        :rtype: ~computervision.models.TagResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            return self.vision.tag_image(
                url=url,
                language=language,
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
        except ComputerVisionErrorException as error:
            raise error

    def generate_thumbnail(self, width, height, url, smart_cropping=False, **kwargs):
        """This operation generates a thumbnail image with the user-specified
        width and height. By default, the service analyzes the image,
        identifies the region of interest (ROI), and generates smart cropping
        coordinates based on the ROI. Smart cropping helps when you specify an
        aspect ratio that differs from that of the input image.
        A successful response contains the thumbnail image binary. If the
        request failed, the response contains an error code and a message to
        help determine what went wrong.
        Upon failure, the error code and an error message are returned. The
        error code could be one of InvalidImageUrl, InvalidImageFormat,
        InvalidImageSize, InvalidThumbnailSize, NotSupportedImage,
        FailedToProcess, Timeout, or InternalServerError.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param width: Width of the thumbnail, in pixels. It must be between 1
         and 1024. Recommended minimum of 50.
        :type width: int
        :param height: Height of the thumbnail, in pixels. It must be between
         1 and 1024. Recommended minimum of 50.
        :type height: int
        :param smart_cropping: Boolean flag for enabling smart cropping.
        :type smart_cropping: bool
        :return: Generator
        :rtype: ~azure.core.pipeline.transport.requests_basic.StreamDownloadGenerator
        :raises: :class:`HttpResponseError<azure.core.HttpResponseError>`
        """
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
        """This operation returns a bounding box around the most important area of
        the image.
        A successful response will be returned in JSON. If the request failed,
        the response contains an error code and a message to help determine
        what went wrong.
        Upon failure, the error code and an error message are returned. The
        error code could be one of InvalidImageUrl, InvalidImageFormat,
        InvalidImageSize, NotSupportedImage, FailedToProcess, Timeout, or
        InternalServerError.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :return: AreaOfInterestResult
        :rtype: ~computervision.models.AreaOfInterestResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
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
        """Recognize Text operation.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :param mode: Type of text to recognize. Possible values include:
         'Handwritten', 'Printed'
        :type mode: str or ~ocr.models.TextRecognitionMode
        :return: A poller object
        :rtype: ~azure.core.polling.LROPoller
        :raises:
         :class:`ComputerVisionErrorException<ocr.models.ComputerVisionErrorException>`
        """
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
        """Use this interface to get the result of a Read operation, employing the
        state-of-the-art Optical Character Recognition (OCR) algorithms
        optimized for text-heavy documents.

        :param data: Publicly reachable URL of an image or an image stream.
        :type data: str or bytes
        :return: A poller object
        :rtype: ~azure.core.polling.LROPoller
        :raises:
         :class:`ComputerVisionErrorException<ocr.models.ComputerVisionErrorException>`
        """
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