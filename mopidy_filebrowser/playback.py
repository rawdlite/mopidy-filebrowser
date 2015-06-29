from __future__ import unicode_literals

import logging

from mopidy import backend
from mopidy.utils import path

from uritools import urisplit

logger = logging.getLogger(__name__)


class FileBrowserPlaybackProvider(backend.PlaybackProvider):

    def __init__(self, *args, **kwargs):
        super(FileBrowserPlaybackProvider, self).__init__(*args, **kwargs)

    def translate_uri(self, uri):
        logger.debug('translate_uri called %s', uri)
        # import pdb; pdb.set_trace()
        local_uri = path.path_to_uri(urisplit(uri).path)
        logger.debug('local_uri: %s' % local_uri)
        return local_uri
