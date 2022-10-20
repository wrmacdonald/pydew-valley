import pygame
from os import walk


def import_folder(path):
    surface_list = []

    # walk through folders & subfolders to get list of filenames
    for folder_name, sub_folder, image_files in walk(path):
        for image in sorted(image_files):
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    """ for importing files when need to get specific names """
    surface_dict = {}    # key: file name, value: corresponding file

    for folder_name, sub_folder, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict
