import pygame as pg
from os import path

class ImageLoader:
    def __call__(self, pathname: str) -> pg.Surface:
        return pg.image.load(path.abspath(pathname))

image_load = ImageLoader()
