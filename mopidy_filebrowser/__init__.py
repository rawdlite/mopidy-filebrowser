from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext


__version__ = '0.0.1'

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-Filebrowser'
    ext_name = 'filebrowser'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['media_dir'] = config.List()
        schema['show_hidden'] = config.Boolean()
        schema['follow_symlinks'] = config.Boolean()
        return schema

    def setup(self, registry):
        from mopidy_filebrowser.backend import FileBrowserBackend

        registry.add('backend', FileBrowserBackend)
