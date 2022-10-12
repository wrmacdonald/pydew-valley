import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class SoilLayer:
    def __init__(self, all_sprites):
        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load('../graphics/soil/o.png')
        self.soil_surfs = import_folder_dict('../graphics/soil/')

        # requirements
        # if area is farmable
        # if soil has been watered
        # if soil already has a plant

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('../graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        # list of lists for each tile (row & col) in map
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../data/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                # check is tile farmable?
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    # used hoe on a farmable tile
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        # get rid of existing soil patches & redraw them
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # create auto-tiling
                    # tile options surrounding
                    t = 'X' in self.grid[index_row - 1][index_col]
                    b = 'X' in self.grid[index_row + 1][index_col]
                    r = 'X' in row[index_col + 1]
                    l = 'X' in row[index_col - 1]

                    # default tile
                    tile_type = 'o'

                    # all sides
                    if all((t, b, r, l)): tile_type = 'x'

                    SoilTile(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf=self.soil_surfs[tile_type],
                        groups=[self.all_sprites, self.soil_sprites]
                    )
