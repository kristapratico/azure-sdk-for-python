# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
# pylint: disable=no-self-use

from .models import ImageDescription


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
