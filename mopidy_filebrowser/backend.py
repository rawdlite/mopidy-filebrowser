from __future__ import unicode_literals

import logging

from mopidy import backend

import pykka

from mopidy_filebrowser import library, playback

logger = logging.getLogger(__name__)


class FileBrowserBackend(pykka.ThreadingActor, backend.Backend):

    def __init__(self, config, audio):
        super(FileBrowserBackend, self).__init__()
        self.media_dirs = []
        for entry in config['filebrowser']['media_dir']:
            media_dir = {}
            media_dict = entry.split(':')
            media_dir['path'] = media_dict[0]
            if len(media_dict) == 2:
                media_dir['name'] = media_dict[1]
            else:
                media_dir['name'] = media_dict[0]
            self.media_dirs.append(media_dir)
        logger.debug(self.media_dirs)
        self._follow_symlinks = config['filebrowser']['follow_symlinks']
        self._show_hidden = config['filebrowser']['show_hidden']
        self.playback = playback.FileBrowserPlaybackProvider(audio=audio,
                                                             backend=self)
        self.library = library.FileBrowserLibraryProvider(backend=self)
        self.playlists = None
        self.uri_schemes = ['filebrowser']
