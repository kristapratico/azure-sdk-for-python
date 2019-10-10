from .models import (
    DetectedObject,
    BoundingRect,
    ObjectHierarchy,
    ImageAnalysis,
    Category,
    AdultInfo,
    ColorInfo,
    ImageType,
    ImageTag,
    ImageDescriptionDetails,
    FaceDescription,
    DetectedBrand,
    ImageMetadata
)

def response_handler(response, deserialized, response_headers):
    return response


def deserialize_detected_objects(response, obj, response_headers):
    detected_objects = []
    for detected_obj in obj.objects:
        detected_objects.append(
            DetectedObject(
                rectangle=BoundingRect._from_generated(detected_obj.rectangle),
                object_property=detected_obj.object_property,
                confidence=detected_obj.confidence,
                parent=ObjectHierarchy._from_generated(detected_obj.parent)
            )
        )
    return detected_objects


def deserialize_image_analysis(response, obj, response_headers):
    return ImageAnalysis(
        categories=Category._from_generated(obj.categories),
        adult=AdultInfo._from_generated(obj.adult),
        color=ColorInfo._from_generated(obj.color),
        image_type=ImageType._from_generated(obj.image_type),
        tags=ImageTag._from_generated(obj.tags),
        description=ImageDescriptionDetails._from_generated(obj.description),
        faces=FaceDescription._from_generated(obj.faces),
        objects=[DetectedObject._from_generated(object) for object in obj.objects],
        brands=[DetectedBrand._from_generated(brand) for brand in obj.brands],
        request_id=obj.request_id,
        metadata=ImageMetadata._from_generated(obj.metadata),
    )