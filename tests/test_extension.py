from __future__ import unicode_literals

from mopidy_filebrowser import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert '[filebrowser]' in config
    assert 'enabled = true' in config
    assert 'show_hidden = False' in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()
    assert 'show_hidden' in schema
    assert 'follow_symlinks' in schema
    assert 'media_dir' in schema
