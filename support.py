import pygame.image
from pathlib import Path


def import_folder(path):
    return [pygame.image.load(file) for file in Path(path).iterdir() if Path(file).is_file()]
