import pygame

from settings import *
from tile import *
from player import *
from support import *

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # creates map from file and sets boundaries
        layout = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv')
        }
        for style, layout in layout.items():
            for row_index, row in enumerate(WORLD_MAP):
                for col_index, col in enumerate(row):
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    if style == 'boundary':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'invisible')

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # create the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # get the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draws the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
