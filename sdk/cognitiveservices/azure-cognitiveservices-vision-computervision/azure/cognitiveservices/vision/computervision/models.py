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