# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import functools
import six
import io
from typing import (  # pylint: disable=unused-import
    Union, Optional, Any, IO, Iterable, AnyStr, Dict, List, Tuple, Generator,
    TYPE_CHECKING
)
from azure.core.polling import LROPoller
from azure.core.tracing.decorator import distributed_trace
from ._generated._computer_vision_client import ComputerVisionClient as ComputerVision
from ._generated.models import ComputerVisionErrorException
from ._polling import ComputerVisionPollingMethod
from ._base_client import ComputerVisionClientBase

from ._deserialize import deserialize_image_description_results, deserialize_color_results,deserialize_face_results

if TYPE_CHECKING:
    from azure.cognitiveservices.vision.computervision._generated.models import (
        VisualFeatureTypes,
        Details,
    )
    from azure.cognitiveservices.vision.computervision._generated.models import (
        ImageAnalysis,
        ImageDescription,
        DetectResult,
        ListModelsResult,
        OcrResult,
        TagResult,
        AreaOfInterestResult,
        TextRecognitionMode,
    )

def response_handler(response, deserialized, response_headers):
    return response


class ComputerVisionClient(ComputerVisionClientBase):
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
    def __init__(self, endpoint, credential, **kwargs):
        # type: (str, str, Any) -> None
        super(ComputerVisionClient, self).__init__(credentials=credential, **kwargs)
        self._client = ComputerVision(
            endpoint=endpoint, credentials=credential, pipeline=self._pipeline)

    def analyze_image(
            self, image_or_url,  # type: Union[str, io.BufferedReader]
            visual_features=None,  # type: Optional[Union[List[str], VisualFeatureTypes]]
            details=None,  # type: Optional[List[str, Details]]
            language="en",  # type: Optional[str]
            **kwargs  # type: Any
        ):  # type: (...) -> ImageAnalysis
        """This operation extracts a rich set of visual features based on the
        image content.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL. Within your request, there is an optional
        parameter to allow you to choose which features to return. By default,
        image categories are returned in the response.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
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
        try:
            if isinstance(image_or_url, six.text_type):
                return self._client.analyze_image(
                    url=image_or_url,
                    visual_features=visual_features,
                    details=details,
                    language=language,
                    description_exclude=kwargs.pop("description_exclude", None),
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            if hasattr(image_or_url, "read"):
                return self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=visual_features,
                    details=details,
                    language=language,
                    description_exclude=kwargs.pop("description_exclude", None),
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def detect_colors(self, image_or_url, language="en", **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["Color"],
                    language=language,
                    cls=deserialize_color_results,
                    **kwargs,
                )
                return resp
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["Color"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.color
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def detect_faces(self, image_or_url, language="en", **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["Faces"],
                    language=language,
                    cls=deserialize_face_results,
                    **kwargs,
                )
                return resp
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["Faces"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.faces
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def detect_adult_content(self, image_or_url, language="en", **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["Adult"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.adult
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["Adult"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.adult
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def detect_brands(self, image_or_url, **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["Brands"],
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.brands
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["Brands"],
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.brands
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def detect_image_type(self, image_or_url, language="en", **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["ImageType"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.image_type
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["ImageType"],
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.image_type
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def detect_categories(self, image_or_url, language="en", details=None, description_exclude=None, **kwargs):
        if isinstance(image_or_url, six.text_type):
            try:
                resp = self._client.analyze_image(
                    url=image_or_url,
                    visual_features=["Categories"],
                    language=language,
                    details=details,
                    description_exclude=description_exclude,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.categories
            except ComputerVisionErrorException as error:
                raise error
        if hasattr(image_or_url, "read"):
            try:
                resp = self._client.analyze_image_in_stream(
                    image=image_or_url,
                    visual_features=["Categories"],
                    language=language,
                    details=details,
                    description_exclude=description_exclude,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.categories
            except ComputerVisionErrorException as error:
                raise error
        else:
            raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))

    def describe_image(
            self, image_or_url,  # type: Union[str, io.BufferedReader]
            max_candidates=1,  # type: Optional[int]
            language="en",  # type: Optional[str]
            **kwargs  # type: Any
        ):  # type: (...) -> ImageDescription
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

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or io.BinaryIO
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
            if isinstance(image_or_url, six.text_type):
                return self._client.describe_image(
                    url=image_or_url,
                    max_candidates=max_candidates,
                    language=language,
                    description_exclude=kwargs.pop("description_exclude", None),
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            if hasattr(image_or_url, "read"):
                return self._client.describe_image_in_stream(
                    image=image_or_url,
                    max_candidates=max_candidates,
                    language=language,
                    description_exclude=kwargs.pop("description_exclude", None),
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def detect_objects(self, image_or_url, **kwargs):
        # type: (Union[str, io.BufferedReader], Any) -> DetectResult
        """Performs object detection on the specified image.
        Two input methods are supported -- (1) Uploading an image or (2)
        specifying an image URL.
        A successful response will be returned in JSON. If the request failed,
        the response will contain an error code and a message to help
        understand what went wrong.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or io.BinaryIO
        :return: DetectResult
        :rtype: ~computervision.models.DetectResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            if isinstance(image_or_url, six.text_type):
                response = self._client.detect_objects(
                    url=image_or_url,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return response.objects
            if hasattr(image_or_url, "read"):
                response = self._client.detect_objects_in_stream(
                    image=image_or_url,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return response.objects
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def list_models(self, **kwargs):
        # type: (Any) -> ListModelsResult
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
            response = self._client.list_models(
                cls=kwargs.pop("cls", None),
                **kwargs,
            )
            return response.models_property
        except ComputerVisionErrorException as error:
            raise error

    def analyze_image_by_domain(self, image_or_url, model, language="en", **kwargs):
        # type: (Union[str, io.BufferedReader], str, Optional[str], Any) -> List[Dict]
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

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
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
            if isinstance(image_or_url, six.text_type):
                resp = self._client.analyze_image_by_domain(
                    url=image_or_url,
                    model=model,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return resp.result[model]
            if hasattr(image_or_url, "read"):
                return self._client.analyze_image_by_domain_in_stream(
                    image=image_or_url,
                    model=model,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def recognize_printed_text(self, image_or_url, detect_orientation=True, language="unk", **kwargs):
        # type: (Union[str, io.BufferedReader], Optional[bool], Optional[str], Any) -> OcrResult
        """Optical Character Recognition (OCR) detects text in an image and
        extracts the recognized characters into a machine-usable character
        stream.
        Upon success, the OCR results will be returned.
        Upon failure, the error code together with an error message will be
        returned. The error code can be one of InvalidImageUrl,
        InvalidImageFormat, InvalidImageSize, NotSupportedImage,
        NotSupportedLanguage, or InternalServerError.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
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
            if isinstance(image_or_url, six.text_type):
                return self._client.recognize_printed_text(
                    url=image_or_url,
                    detect_orientation=detect_orientation,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            if hasattr(image_or_url, "read"):
                return self._client.recognize_printed_text_in_stream(
                    image=image_or_url,
                    detect_orientation=detect_orientation,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def tag_image(self, image_or_url, language="en", **kwargs):
        # type: (Union[str, io.BufferedReader], Optional[str], Any) -> TagResult
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

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
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
            if isinstance(image_or_url, six.text_type):
                tag_result = self._client.tag_image(
                    url=image_or_url,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return tag_result.tags
            if hasattr(image_or_url, "read"):
                tag_result = self._client.tag_image_in_stream(
                    image=image_or_url,
                    language=language,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return tag_result.tags
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def generate_thumbnail(self, image_or_url, width, height, smart_cropping=False, **kwargs):
        # type: (Union[str, io.BufferedReader], int, int, Optional[bool], Any) -> Generator
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

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
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
            if isinstance(image_or_url, six.text_type):
                return self._client.generate_thumbnail(
                    url=image_or_url,
                    width=width,
                    height=height,
                    smart_cropping=smart_cropping,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            if hasattr(image_or_url, "read"):
                return self._client.generate_thumbnail_in_stream(
                    image=image_or_url,
                    width=width,
                    height=height,
                    smart_cropping=smart_cropping,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def get_area_of_interest(self, image_or_url, **kwargs):
        # type: (Union[str, io.BufferedReader], Any) -> AreaOfInterestResult
        """This operation returns a bounding box around the most important area of
        the image.
        A successful response will be returned in JSON. If the request failed,
        the response contains an error code and a message to help determine
        what went wrong.
        Upon failure, the error code and an error message are returned. The
        error code could be one of InvalidImageUrl, InvalidImageFormat,
        InvalidImageSize, NotSupportedImage, FailedToProcess, Timeout, or
        InternalServerError.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
        :return: AreaOfInterestResult
        :rtype: ~computervision.models.AreaOfInterestResult
        :raises:
         :class:`ComputerVisionErrorException<computervision.models.ComputerVisionErrorException>`
        """
        try:
            if isinstance(image_or_url, six.text_type):
                response = self._client.get_area_of_interest(
                    url=image_or_url,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return response.area_of_interest
            if hasattr(image_or_url, "read"):
                response = self._client.get_area_of_interest_in_stream(
                    image=image_or_url,
                    cls=kwargs.pop("cls", None),
                    **kwargs,
                )
                return response.area_of_interest
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

    def recognize_text(self, image_or_url, mode, **kwargs):
        # type: (Union[str, io.BufferedReader], Union[str, TextRecognitionMode], Any) -> LROPoller
        """Recognize Text operation.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
        :param mode: Type of text to recognize. Possible values include:
         'Handwritten', 'Printed'
        :type mode: str or ~ocr.models.TextRecognitionMode
        :return: A poller object
        :rtype: ~azure.core.polling.LROPoller
        :raises:
         :class:`ComputerVisionErrorException<ocr.models.ComputerVisionErrorException>`
        """
        try:
            if isinstance(image_or_url, six.text_type):
                job = self._client.recognize_text(
                    url=image_or_url,
                    mode=mode,
                    cls=response_handler,
                    **kwargs,
                )
            elif hasattr(image_or_url, "read"):
                job = self._client.recognize_text_in_stream(
                    image=image_or_url,
                    mode=mode,
                    cls=response_handler,
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self._client.get_text_operation_result,
            operation_id,
        )

        start_recognize_text = command()
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_recognize_text, None, polling_method)

    def batch_read_file(self, image_or_url, **kwargs):
        # type: (Union[str, io.BufferedReader], Any) -> LROPoller
        """Use this interface to get the result of a Read operation, employing the
        state-of-the-art Optical Character Recognition (OCR) algorithms
        optimized for text-heavy documents.

        :param image_or_url: Publicly reachable URL of an image or an image stream.
        :type image_or_url: str or bytes
        :return: A poller object
        :rtype: ~azure.core.polling.LROPoller
        :raises:
         :class:`ComputerVisionErrorException<ocr.models.ComputerVisionErrorException>`
        """
        try:
            if isinstance(image_or_url, six.text_type):
                job = self._client.batch_read_file(
                    url=image_or_url,
                    cls=response_handler,
                    **kwargs,
                )
            elif hasattr(image_or_url, "read"):
                job = self._client.batch_read_file_in_stream(
                    image=image_or_url,
                    cls=response_handler,
                    **kwargs,
                )
            else:
                raise TypeError("Unsupported image_or_url type: {}".format(type(image_or_url)))
        except ComputerVisionErrorException as error:
            raise error

        operation_id = job.headers["Operation-Location"].split("/")[-1]

        command = functools.partial(
            self._client.get_read_operation_result,
            operation_id,
        )

        start_batch_read_file = command()
        polling_method = ComputerVisionPollingMethod(1)  # what should polling interval be set to?
        return LROPoller(command, start_batch_read_file, None, polling_method)
