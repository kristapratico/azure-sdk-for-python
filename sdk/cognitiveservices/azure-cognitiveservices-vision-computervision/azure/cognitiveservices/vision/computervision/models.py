# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from ._generated.models._models import ImageDescription as GeneratedImageDescription


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