# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from ._generated.models._models import ImageDescription as GeneratedImageDescription
from ._generated.models._models import ColorInfo as GeneratedColorInfo
from ._generated.models._models import FaceDescription as GeneratedFaceDescription

class ImageDescription(GeneratedImageDescription):
    """A collection of content tags, along with a list of captions sorted by
    confidence level, and image metadata.

    :param tags: A collection of image tags.
    :type tags: list[str]
    :param captions: A list of captions, sorted by confidence level.
    :type captions: list[~computervision.models.ImageCaption]
    :param request_id: Id of the REST API request.
    :type request_id: str
    :param metadata:
    :type metadata: ~computervision.models.ImageMetadata
    """
    def __init__(self, **kwargs):
        self.tags = kwargs.get('tags', None)
        self.captions = kwargs.get('captions', None)
        self.request_id = kwargs.get('request_id', None)
        self.metadata = kwargs.get('metadata', None)


class ColorInfo(object):
    """An object providing additional metadata describing color attributes.

    :param dominant_color_foreground: Possible dominant foreground color.
    :type dominant_color_foreground: str
    :param dominant_color_background: Possible dominant background color.
    :type dominant_color_background: str
    :param dominant_colors: An array of possible dominant colors.
    :type dominant_colors: list[str]
    :param accent_color: Possible accent color.
    :type accent_color: str
    :param is_bw_img: A value indicating if the image is black and white.
    :type is_bw_img: bool
    """

    def __init__(self, **kwargs):
        self.dominant_color_foreground = kwargs.get('dominant_color_foreground', None)
        self.dominant_color_background = kwargs.get('dominant_color_background', None)
        self.dominant_colors = kwargs.get('dominant_colors', None)
        self.accent_color = kwargs.get('accent_color', None)
        self.is_bw_img = kwargs.get('is_bw_img', None)


class FaceDescription(GeneratedFaceDescription):
    """An object describing a face identified in the image.

    :param age: Possible age of the face.
    :type age: int
    :param gender: Possible gender of the face. Possible values include:
     'Male', 'Female'
    :type gender: str or ~computervision.models.Gender
    :param face_rectangle: Rectangle in the image containing the identified
     face.
    :type face_rectangle: ~computervision.models.FaceRectangle
    """

    _attribute_map = {
        'age': {'key': 'age', 'type': 'int'},
        'gender': {'key': 'gender', 'type': 'Gender'},
        'face_rectangle': {'key': 'faceRectangle', 'type': 'FaceRectangle'},
    }

    def __init__(self, **kwargs):
        self.age = kwargs.get('age', None)
        self.gender = kwargs.get('gender', None)
        self.face_rectangle = kwargs.get('face_rectangle', None)


class OcrResult(object):
    """OcrResult.

    :param language: The BCP-47 language code of the text in the image.
    :type language: str
    :param text_angle: The angle, in radians, of the detected text with
     respect to the closest horizontal or vertical direction. After rotating
     the input image clockwise by this angle, the recognized text lines become
     horizontal or vertical. In combination with the orientation property it
     can be used to overlay recognition results correctly on the original
     image, by rotating either the original image or recognition results by a
     suitable angle around the center of the original image. If the angle
     cannot be confidently detected, this property is not present. If the image
     contains text at different angles, only part of the text will be
     recognized correctly.
    :type text_angle: float
    :param orientation: Orientation of the text recognized in the image, if
     requested. The value (up, down, left, or right) refers to the direction
     that the top of the recognized text is facing, after the image has been
     rotated around its center according to the detected text angle (see
     textAngle property).
     If detection of the orientation was not requested, or no text is detected,
     the value is 'NotDetected'.
    :type orientation: str
    :param regions: An array of objects, where each object represents a region
     of recognized text.
    :type regions: list[~computervision.models.OcrRegion]
    """

    def __init__(self, **kwargs):
        self.language = kwargs.get('language', None)
        self.text_angle = kwargs.get('text_angle', None)
        self.orientation = kwargs.get('orientation', None)
        self.regions = kwargs.get('regions', None)
        self.full_text = kwargs.get('full_text', None)


class TextRecognitionResult(object):
    """An object representing a recognized text region.

    All required parameters must be populated in order to send to Azure.

    :param page: The 1-based page number of the recognition result.
    :type page: int
    :param clockwise_orientation: The orientation of the image in degrees in
     the clockwise direction. Range between [0, 360).
    :type clockwise_orientation: float
    :param width: The width of the image in pixels or the PDF in inches.
    :type width: float
    :param height: The height of the image in pixels or the PDF in inches.
    :type height: float
    :param unit: The unit used in the Width, Height and BoundingBox. For
     images, the unit is 'pixel'. For PDF, the unit is 'inch'. Possible values
     include: 'pixel', 'inch'
    :type unit: str or ~ocr.models.TextRecognitionResultDimensionUnit
    :param lines: Required. A list of recognized text lines.
    :type lines: list[~ocr.models.Line]
    """

    def __init__(self, **kwargs):
        self.page = kwargs.get('page', None)
        self.clockwise_orientation = kwargs.get('clockwise_orientation', None)
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.unit = kwargs.get('unit', None)
        self.lines = kwargs.get('lines', None)
        self.full_text = kwargs.get('full_text', None)