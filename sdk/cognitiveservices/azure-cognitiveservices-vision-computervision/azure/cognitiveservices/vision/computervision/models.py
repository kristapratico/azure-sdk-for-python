# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from enum import Enum


class Gender(str, Enum):

    male = "Male"
    female = "Female"


class DescriptionExclude(str, Enum):

    celebrities = "Celebrities"
    landmarks = "Landmarks"


class AdultInfo(object):
    """An object describing whether the image contains adult-oriented content
    and/or is racy.

    :param is_adult_content: A value indicating if the image contains
     adult-oriented content.
    :type is_adult_content: bool
    :param is_racy_content: A value indicating if the image is racy.
    :type is_racy_content: bool
    :param is_gory_content: A value indicating if the image is gory.
    :type is_gory_content: bool
    :param adult_score: Score from 0 to 1 that indicates how much the content
     is considered adult-oriented within the image.
    :type adult_score: float
    :param racy_score: Score from 0 to 1 that indicates how suggestive is the
     image.
    :type racy_score: float
    :param gore_score: Score from 0 to 1 that indicates how gory is the image.
    :type gore_score: float
    """

    def __init__(self, **kwargs):
        self.is_adult_content = kwargs.get('is_adult_content', None)
        self.is_racy_content = kwargs.get('is_racy_content', None)
        self.is_gory_content = kwargs.get('is_gory_content', None)
        self.adult_score = kwargs.get('adult_score', None)
        self.racy_score = kwargs.get('racy_score', None)
        self.gore_score = kwargs.get('gore_score', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            is_adult_content=obj.is_adult_content,
            is_racy_content=obj.is_racy_content,
            is_gory_content=obj.is_gory_content,
            adult_score=obj.adult_score,
            racy_score=obj.racy_score,
            gore_score=obj.gore_score,
        )


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
            dominant_color_foreground=obj.dominant_color_foreground,
            dominant_color_background=obj.dominant_color_background,
            dominant_colors=obj.dominant_colors,
            accent_color=obj.accent_color,
            is_bw_img=obj.is_bw_img,
        )


class DetectedBrand(object):
    """A brand detected in an image.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar name: Label for the brand.
    :vartype name: str
    :ivar confidence: Confidence score of having observed the brand in the
     image, as a value ranging from 0 to 1.
    :vartype confidence: float
    :ivar rectangle: Approximate location of the detected brand.
    :vartype rectangle: ~computervision.models.BoundingRect
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.confidence = kwargs.get('confidence', None)
        self.rectangle = kwargs.get('rectangle', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            name=obj.name,
            confidence=obj.confidence,
            rectangle=BoundingRect._from_generated(obj.rectangle)
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


class BoundingRect(object):
    """A bounding box for an area inside an image.

    :param x: X-coordinate of the top left point of the area, in pixels.
    :type x: int
    :param y: Y-coordinate of the top left point of the area, in pixels.
    :type y: int
    :param w: Width measured from the top-left point of the area, in pixels.
    :type w: int
    :param h: Height measured from the top-left point of the area, in pixels.
    :type h: int
    """

    def __init__(self, **kwargs):
        self.x = kwargs.get('x', None)
        self.y = kwargs.get('y', None)
        self.w = kwargs.get('w', None)
        self.h = kwargs.get('h', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            x=obj.x,
            y=obj.y,
            w=obj.w,
            h=obj.h
        )


class Category(object):
    """An object describing identified category.

    :param name: Name of the category.
    :type name: str
    :param score: Scoring of the category.
    :type score: float
    :param detail: Details of the identified category.
    :type detail: ~computervision.models.CategoryDetail
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.score = kwargs.get('score', None)
        self.detail = kwargs.get('detail', None)

    @classmethod
    def _from_generated(cls, obj):
        if obj is None:
            return obj
        return [cls(
            name=cat.name,
            score=cat.score,
            detail=CategoryDetail._from_generated(cat.detail),
            ) for cat in obj]


class CategoryDetail(object):
    """An object describing additional category details.

    :param celebrities: An array of celebrities if any identified.
    :type celebrities: list[~computervision.models.CelebritiesModel]
    :param landmarks: An array of landmarks if any identified.
    :type landmarks: list[~computervision.models.LandmarksModel]
    """
    def __init__(self, **kwargs):
        self.celebrities = kwargs.get('celebrities', None)
        self.landmarks = kwargs.get('landmarks', None)

    @classmethod
    def _from_generated(cls, obj):
        if obj is None:
            return obj

        if obj.landmarks is None:
            return cls(
                celebrities=[CelebritiesModel._from_generated(celeb) for celeb in obj.celebrities],
                landmarks=None
            )

        if obj.celebrities is None:
            return cls(
                celebrities=None,
                landmarks=[LandmarksModel._from_generated(landmark) for landmark in obj.landmarks]
            )

        return cls(
            celebrities=[CelebritiesModel._from_generated(celeb) for celeb in obj.celebrities],
            landmarks=[LandmarksModel._from_generated(landmark) for landmark in obj.landmarks]
        )


class CelebritiesModel(object):
    """An object describing possible celebrity identification.

    :param name: Name of the celebrity.
    :type name: str
    :param confidence: Confidence level for the celebrity recognition as a
     value ranging from 0 to 1.
    :type confidence: float
    :param face_rectangle: Location of the identified face in the image.
    :type face_rectangle: ~computervision.models.FaceRectangle
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.confidence = kwargs.get('confidence', None)
        self.face_rectangle = kwargs.get('face_rectangle', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            name=obj.name,
            confidence=obj.confidence,
            face_rectangle=FaceRectangle._from_generated(obj.face_rectangle),
        )


class FaceDescription(object):
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

    def __init__(self, **kwargs):
        self.age = kwargs.get('age', None)
        self.gender = kwargs.get('gender', None)
        self.face_rectangle = kwargs.get('face_rectangle', None)

    @classmethod
    def _from_generated(cls, obj):
        if obj is None:
            return obj
        return [cls(
                age=face.age,
                gender=Gender(face.gender),
                face_rectangle=FaceRectangle._from_generated(face.face_rectangle),
                ) for face in obj]


class FaceRectangle(object):
    """An object describing face rectangle.

    :param left: X-coordinate of the top left point of the face, in pixels.
    :type left: int
    :param top: Y-coordinate of the top left point of the face, in pixels.
    :type top: int
    :param width: Width measured from the top-left point of the face, in
     pixels.
    :type width: int
    :param height: Height measured from the top-left point of the face, in
     pixels.
    :type height: int
    """

    def __init__(self, **kwargs):
        self.left = kwargs.get('left', None)
        self.top = kwargs.get('top', None)
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            left=obj.left,
            top=obj.top,
            width=obj.width,
            height=obj.height
        )


class ImageCaption(object):
    """An image caption, i.e. a brief description of what the image depicts.

    :param text: The text of the caption.
    :type text: str
    :param confidence: The level of confidence the service has in the caption.
    :type confidence: float
    """

    def __init__(self, **kwargs):
        self.text = kwargs.get('text', None)
        self.confidence = kwargs.get('confidence', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            text=obj.text,
            confidence=obj.confidence
        )


class ImageDescriptionDetails(object):
    """A collection of content tags, along with a list of captions sorted by
    confidence level, and image metadata.

    :param tags: A collection of image tags.
    :type tags: list[str]
    :param captions: A list of captions, sorted by confidence level.
    :type captions: list[~computervision.models.ImageCaption]
    """

    def __init__(self, **kwargs):
        self.tags = kwargs.get('tags', None)
        self.captions = kwargs.get('captions', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            tags=obj.tags,
            captions=[ImageCaption._from_generated(caption) for caption in obj.captions]
        )


class ImageMetadata(object):
    """Image metadata.

    :param width: Image width, in pixels.
    :type width: int
    :param height: Image height, in pixels.
    :type height: int
    :param format: Image format.
    :type format: str
    """

    def __init__(self, **kwargs):
        self.width = kwargs.get('width', None)
        self.height = kwargs.get('height', None)
        self.format = kwargs.get('format', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            width=obj.width,
            height=obj.height,
            format=obj.format
        )

class ImageTag(object):
    """An entity observation in the image, along with the confidence score.

    :param name: Name of the entity.
    :type name: str
    :param confidence: The level of confidence that the entity was observed.
    :type confidence: float
    :param hint: Optional hint/details for this tag.
    :type hint: str
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.confidence = kwargs.get('confidence', None)
        self.hint = kwargs.get('hint', None)

    @classmethod
    def _from_generated(cls, obj):
        return [cls(
            name=tag.name,
            confidence=tag.confidence,
            hint=tag.hint,
        ) for tag in obj]

class ImageType(object):
    """An object providing possible image types and matching confidence levels.

    :param clip_art_type: Confidence level that the image is a clip art.
    :type clip_art_type: int
    :param line_drawing_type: Confidence level that the image is a line
     drawing.
    :type line_drawing_type: int
    """

    def __init__(self, **kwargs):
        self.clip_art_type = kwargs.get('clip_art_type', None)
        self.line_drawing_type = kwargs.get('line_drawing_type', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            clip_art_type=obj.clip_art_type,
            line_drawing_type=obj.line_drawing_type
        )

class LandmarksModel(object):
    """A landmark recognized in the image.

    :param name: Name of the landmark.
    :type name: str
    :param confidence: Confidence level for the landmark recognition as a
     value ranging from 0 to 1.
    :type confidence: float
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.confidence = kwargs.get('confidence', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            name=obj.name,
            confidence=obj.confidence,
        )


class ObjectHierarchy(object):
    """An object detected inside an image.

    :param object_property: Label for the object.
    :type object_property: str
    :param confidence: Confidence score of having observed the object in the
     image, as a value ranging from 0 to 1.
    :type confidence: float
    :param parent: The parent object, from a taxonomy perspective.
     The parent object is a more generic form of this object.  For example, a
     'bulldog' would have a parent of 'dog'.
    :type parent: ~computervision.models.ObjectHierarchy
    """

    def __init__(self, **kwargs):
        self.object_property = kwargs.get('object_property', None)
        self.confidence = kwargs.get('confidence', None)
        self.parent = kwargs.get('parent', None)

    @classmethod
    def _from_generated(cls, obj):
        if obj is None:
            return
        return cls(
            object_property=obj.object_property,
            confidence=obj.confidence,
            parent=ObjectHierarchy._from_generated(obj.parent),
        )


class DetectedObject(object):
    """An object detected in an image.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar rectangle: Approximate location of the detected object.
    :vartype rectangle: ~computervision.models.BoundingRect
    :param object_property: Label for the object.
    :type object_property: str
    :param confidence: Confidence score of having observed the object in the
     image, as a value ranging from 0 to 1.
    :type confidence: float
    :param parent: The parent object, from a taxonomy perspective.
     The parent object is a more generic form of this object.  For example, a
     'bulldog' would have a parent of 'dog'.
    :type parent: ~computervision.models.ObjectHierarchy
    """
    def __init__(self, **kwargs):
        self.rectangle = kwargs.get('rectangle', None)
        self.object_property = kwargs.get('object_property', None)
        self.confidence = kwargs.get('confidence', None)
        self.parent = kwargs.get('parent', None)

    @classmethod
    def _from_generated(cls, obj):
        return cls(
            rectangle=BoundingRect._from_generated(obj.rectangle),
            object_property=obj.object_property,
            confidence=obj.confidence,
            parent=ObjectHierarchy._from_generated(obj.parent)
        )