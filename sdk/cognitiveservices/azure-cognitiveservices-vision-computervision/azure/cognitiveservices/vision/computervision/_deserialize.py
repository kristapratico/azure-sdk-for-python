# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=no-self-use

from .models import ImageDescription
from .models import ColorInfo
from .models import FaceDescription
from .models import OcrResult
from .models import TextRecognitionResult

def deserialize_image_metadata(response, obj, headers):  # pylint: disable=unused-argument
    raw_metadata = {"width": obj.metadata.width,
                    "height": obj.metadata.height,
                    "format": obj.metadata.format}
    return raw_metadata


# def deserialize_domain_results(response, obj, headers):
#     metadata = deserialize_image_metadata(response, obj, headers)
#     domain_results = DomainModelResults(
#         result=obj.result,
#         # request_id=obj.request_id,
#         # metadata=metadata,
#     )
#
#     return domain_results


def deserialize_img_captions(obj):  # pylint: disable=unused-argument
    raw_captions = []
    for cap in obj.captions:
        raw_captions.append({"text": cap.text, "confidence": cap.confidence})
    return raw_captions


def deserialize_image_description_results(response, obj, headers):
    captions = deserialize_img_captions(obj)
    metadata = deserialize_image_metadata(response, obj, headers)
    img_description_results = ImageDescription(
        tags=obj.tags,
        captions=captions,
        request_id=obj.request_id,
        metadata=metadata,
    )

    return img_description_results


def deserialize_color_results(response, obj, headers):
    # metadata = deserialize_image_metadata(response, obj, headers)
    img_color_results = ColorInfo(
        dominant_color_foreground=obj.color.dominant_color_foreground,
        dominant_color_background=obj.color.dominant_color_background,
        dominant_colors=obj.color.dominant_colors,
        accent_color=obj.color.accent_color,
        is_bw_img=obj.color.is_bw_img,
    )
    # img_color_results.request_id = obj.request_id
    # img_color_results.metadata = metadata
    return img_color_results


def deserialize_face_results(response, obj, headers):
    # metadata = deserialize_image_metadata(response, obj, headers)
    faces = []
    faces_results = obj.faces
    for face in faces_results:
        img_face_results = FaceDescription(
            age=face.age,
            gender=face.gender,
            face_rectangle=face.face_rectangle,
        )
        img_face_results.request_id = obj.request_id
        img_face_results.metadata = obj.metadata
        faces.append(img_face_results)

    return faces


def deserialize_ocr_result(response, obj, headers):
    full_text_result = []
    for lines in obj.regions:
        full_text = ""
        for line in lines.lines:
            line_text = " ".join([word.text for word in line.words])
            full_text += "\n" + line_text

        full_text_result.append(full_text)

    ocr_result = OcrResult(
        language=obj.language,
        text_angle=obj.text_angle,
        orientation=obj.orientation,
        regions=obj.regions,
        full_text=full_text_result
    )
    return ocr_result


def deserialize_text_recognition_result(obj):
    read_result = []
    full_text_result = []
    for image_text in obj:
        full_text = ""
        for line in image_text.lines:
            full_text += "\n" + line.text
        full_text_result.append(full_text)

        text_result = TextRecognitionResult(
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
