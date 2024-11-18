import os
import shutil
import time
import pathlib


class PathAnalyzer:
    EXTENSIONS = {
        'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 
              'h264', 'flv', 'rm', 'swf', 'vob'],

        'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl',
              'cda'],

        'image': ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 
              'tiff'],
    }

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.dirs = []
        self.files = []
        self.total_files = self._total_files()

        self.generator_files = self.get_files_generator()

    def get_dirs(self):
        self.dirs = [subdirs for subdirs in self.path.iterdir() if subdirs.is_dir()]
        return self.get_dirs
    
    @property
    def get_file(self):
        return next(self.generator_files)

    def get_files(self):
        self.files = [files for files in self.path.iterdir() if files.is_file()]
        return self.files

    def _total_files(self):
        return len([files for files in self.path.iterdir() if files.is_file()])

    def get_files_generator(self):
        for object in self.path.iterdir():
            if object.is_file():
                yield object
