# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------


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

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            dominant_color_foreground=obj.color.dominant_color_foreground,
            dominant_color_background=obj.color.dominant_color_background,
            dominant_colors=obj.color.dominant_colors,
            accent_color=obj.color.accent_color,
            is_bw_img=obj.color.is_bw_img,
        )


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
    :param str full_text: The full recognized text in the image.
    """

    def __init__(self, **kwargs):
        self.language = kwargs.get('language', None)
        self.text_angle = kwargs.get('text_angle', None)
        self.orientation = kwargs.get('orientation', None)
        self.regions = kwargs.get('regions', None)
        self.full_text = kwargs.get('full_text', None)

    @classmethod
    def _from_generated(cls, obj):
        full_text_result = []
        for lines in obj.regions:
            full_text = ""
            for line in lines.lines:
                line_text = " ".join([word.text for word in line.words])
                full_text += "\n" + line_text

            full_text_result.append(full_text)

        return cls(
            language=obj.language,
            text_angle=obj.text_angle,
            orientation=obj.orientation,
            regions=obj.regions,
            full_text=full_text_result
        )


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

    @classmethod
    def _from_generated(cls, obj):
        read_result = []
        full_text_result = []
        for image_text in obj:
            full_text = ""
            for line in image_text.lines:
                full_text += "\n" + line.text
            full_text_result.append(full_text)

            text_result = cls(
                page=image_text.page,
                clockwise_orientation=image_text.clockwise_orientation,
                width=image_text.width,
                height=image_text.height,
                unit=image_text.unit,
                lines=image_text.lines,
                full_text=full_text_result
            )
            read_result.append(text_result)
        return read_result


class ImageAnalysis(object):
    """Result of AnalyzeImage operation.

    :param categories: An array indicating identified categories.
    :type categories: list[~computervision.models.Category]
    :param adult: An object describing whether the image contains
     adult-oriented content and/or is racy.
    :type adult: ~computervision.models.AdultInfo
    :param color: An object providing additional metadata describing color
     attributes.
    :type color: ~computervision.models.ColorInfo
    :param image_type: An object providing possible image types and matching
     confidence levels.
    :type image_type: ~computervision.models.ImageType
    :param tags: A list of tags with confidence level.
    :type tags: list[~computervision.models.ImageTag]
    :param description: A collection of content tags, along with a list of
     captions sorted by confidence level, and image metadata.
    :type description: ~computervision.models.ImageDescriptionDetails
    :param faces: An array of possible faces within the image.
    :type faces: list[~computervision.models.FaceDescription]
    :param objects: Array of objects describing what was detected in the
     image.
    :type objects: list[~computervision.models.DetectedObject]
    :param brands: Array of brands detected in the image.
    :type brands: list[~computervision.models.DetectedBrand]
    :param request_id: Id of the REST API request.
    :type request_id: str
    :param metadata:
    :type metadata: ~computervision.models.ImageMetadata
    """

    def __init__(self, **kwargs):
        self.categories = kwargs.get('categories', None)
        self.adult = kwargs.get('adult', None)
        self.color = kwargs.get('color', None)
        self.image_type = kwargs.get('image_type', None)
        self.tags = kwargs.get('tags', None)
        self.description = kwargs.get('description', None)
        self.faces = kwargs.get('faces', None)
        self.objects = kwargs.get('objects', None)
        self.brands = kwargs.get('brands', None)
        self.request_id = kwargs.get('request_id', None)
        self.metadata = kwargs.get('metadata', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            categories=obj.categories,
            adult=obj.adult,
            color=obj.color,
            image_type=obj.image_type,
            tags=obj.tags,
            description=obj.description,
            faces=obj.faces,
            objects=obj.objects,
            brands=obj.brands,
            request_id=obj.request_id,
            metadata=obj.metadata
        )


# # used by CelebritiesModel and FaceDescription
# class FaceRectangle(Model):
#     """An object describing face rectangle.
#
#     :param left: X-coordinate of the top left point of the face, in pixels.
#     :type left: int
#     :param top: Y-coordinate of the top left point of the face, in pixels.
#     :type top: int
#     :param width: Width measured from the top-left point of the face, in
#      pixels.
#     :type width: int
#     :param height: Height measured from the top-left point of the face, in
#      pixels.
#     :type height: int
#     """
#
#     _attribute_map = {
#         'left': {'key': 'left', 'type': 'int'},
#         'top': {'key': 'top', 'type': 'int'},
#         'width': {'key': 'width', 'type': 'int'},
#         'height': {'key': 'height', 'type': 'int'},
#     }
#
#     def __init__(self, **kwargs):
#         super(FaceRectangle, self).__init__(**kwargs)
#         self.left = kwargs.get('left', None)
#         self.top = kwargs.get('top', None)
#         self.width = kwargs.get('width', None)
#         self.height = kwargs.get('height', None)
#
# # used by AreaOfInterestResult
# class BoundingRect(Model):
#     """A bounding box for an area inside an image.
#
#     :param x: X-coordinate of the top left point of the area, in pixels.
#     :type x: int
#     :param y: Y-coordinate of the top left point of the area, in pixels.
#     :type y: int
#     :param w: Width measured from the top-left point of the area, in pixels.
#     :type w: int
#     :param h: Height measured from the top-left point of the area, in pixels.
#     :type h: int
#     """
#
#     _attribute_map = {
#         'x': {'key': 'x', 'type': 'int'},
#         'y': {'key': 'y', 'type': 'int'},
#         'w': {'key': 'w', 'type': 'int'},
#         'h': {'key': 'h', 'type': 'int'},
#     }
#
#     def __init__(self, **kwargs):
#         super(BoundingRect, self).__init__(**kwargs)
#         self.x = kwargs.get('x', None)
#         self.y = kwargs.get('y', None)
#         self.w = kwargs.get('w', None)
#         self.h = kwargs.get('h', None)


# Used by OcrLine, OcrRegion, OcrWord, Line, Word
# :param bounding_box: Bounding box of a recognized region. The four
#  integers represent the x-coordinate of the left edge, the y-coordinate of
#  the top edge, width, and height of the bounding box, in the coordinate
#  system of the input image, after it has been rotated around its center
#  according to the detected text angle (see textAngle property), with the
#  origin at the top-left corner, and the y-axis pointing down.
# :type bounding_box: str


# OcrLine vs Line (has a text field for the entire line)
# OcrWord vs Word (has a confidence)