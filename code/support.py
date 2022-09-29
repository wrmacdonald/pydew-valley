import pygame
from os import walk


def import_folder(path):
    surface_list = []

    # walk through folders & subfolders to get list of filenames
    for folder_name, sub_folder, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
