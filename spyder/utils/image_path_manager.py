# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

# Standard library imports
import os
import os.path as osp

# Local imports
from spyder.config.base import get_module_data_path, get_module_path
from spyder.config.gui import is_dark_interface

# =============================================================================
# Image path list
# =============================================================================


class ImagePathManager():
    """Manager of the image path in the project."""
    def __init__(self):
        """Initialize the path with all the images."""
        self.IMG_PATH = {}
        self.add_image_path(get_module_data_path('spyder', relpath='images'))
        self.default = 'not_found'

    def add_image_path(self, path):
        """Add path to the image path list."""
        if not osp.isdir(path):
            return

        for dirpath, __, _filenames in os.walk(path):
            if is_dark_interface() and osp.basename(dirpath) == 'light':
                continue
            elif not is_dark_interface() and osp.basename(dirpath) == 'dark':
                continue
            for filename in _filenames:
                name, __ = osp.splitext(osp.basename(filename))
                self.IMG_PATH[name] = osp.join(dirpath, filename)

    def get_image_path(self, name):
        """Get path of the image given the name."""
        try:
            act_image = self.IMG_PATH[name]
            if osp.isfile(act_image):
                return osp.abspath(act_image)
        except KeyError:
            return osp.abspath(self.IMG_PATH[self.default])


IMAGE_PATH_MANAGER = ImagePathManager()


def get_image_path(name):
    """Return image absolute path"""
    return IMAGE_PATH_MANAGER.get_image_path(name)
