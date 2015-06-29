from __future__ import unicode_literals

import logging
import operator
import os
import stat

from mopidy import backend, models
from mopidy.models import Ref

from uritools import uricompose, urisplit

logger = logging.getLogger(__name__)


class FileBrowserLibraryProvider(backend.LibraryProvider):
    URI_PREFIX = 'filebrowser'
    ROOT_URI = URI_PREFIX + ':root'
    root_directory = Ref.directory(uri=ROOT_URI, name='File Browser')

    def __init__(self, *args, **kwargs):
        super(FileBrowserLibraryProvider, self).__init__(*args, **kwargs)

    def browse(self, uri):
        logger.debug(u'browse called with uri %s' % uri)
        result = []
        localpath = urisplit(uri).path
        # import pdb; pdb.set_trace()
        if localpath == 'root':
            result = self._media_dirs()
        else:
            directory = localpath
            logger.debug(u'directory is %s' % directory)
            for name in os.listdir(directory):
                child = os.path.join(directory, name)
                uri = uricompose(self.URI_PREFIX, None, child)
                if self.backend._follow_symlinks:
                    st = os.stat(child)
                else:
                    st = os.lstat(child)
                if not self.backend._show_hidden and name.startswith(b'.'):
                    continue
                elif stat.S_ISDIR(st.st_mode):
                    result.append(models.Ref.directory(name=name, uri=uri))
                elif stat.S_ISREG(st.st_mode):
                    result.append(models.Ref.track(name=name, uri=uri))
                else:
                    logger.warn(u'Strange file encountered %s' % child)
                    pass
        result.sort(key=operator.attrgetter('name'))
        return result

    def lookup(self, uri):
        logger.debug(u'looking up uri = %s' % uri)
        track = models.Track(uri=uri)
        return [track]

    def _media_dirs(self):
        result = []
        for media_dir in self.backend.media_dirs:
            dir = models.Ref.directory(
                name=media_dir['name'],
                uri=uricompose(self.URI_PREFIX, None, media_dir['path']))
            result.append(dir)
        return result
