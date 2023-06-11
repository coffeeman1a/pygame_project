import pygame, random, math as m
from opensimplex import OpenSimplex
from settings import *
from sprites import Tile
from support import import_folder, import_folder_dict

class World():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = CameraGroup()

        # terrain
        # self.grass_surf = []
        # self.sand_surf = []
        # self.shore_surf = []
        # self.water_surf = []
        self.terrain = {}

        # noise parameters
        self.seed = random.randint(0, 100)
        self.noise = OpenSimplex(self.seed)
        self.noise_map = []

        self.setup()

    def setup(self):
        
        for tile_id, tile_name in TILE_TYPE.items():
            self.terrain[tile_name] = import_folder(f'sprites/{tile_name}')

        self.generate_world([20000, 20000])
        self.all_sprites.update_world()

    
    def draw_world_surf(self):
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #sorted by y-axis
                if sprite.z == layer:
                    self.world_surf.blit(sprite.image, sprite.rect)

    def generate_world(self, world_size):

        width = world_size[0]
        height = world_size[1]
        scale = 80
        h_tiles, v_tiles = m.ceil(width / TILE_SIZE), m.ceil(height / TILE_SIZE)
        self.grid = [[[] for col in range (h_tiles)] for row in range(v_tiles)]

        noise = OpenSimplex(random.randint(0, 100))

        # generate tiles
        for row in range(v_tiles):
            for col in range(h_tiles):
                sample_x = row / scale
                sample_y = col / scale

                noise_value = noise.noise2(sample_x, sample_y)
                tile_type = 3  # water by default

                if noise_value > 0.5 and noise_value <= 0.8:
                    tile_type = 3 # shore
                elif noise_value > 0.45 and noise_value <= 0.5:
                    tile_type = 2  # sand
                elif noise_value > -0.7 and noise_value <= 0.45:
                    tile_type = 0  # grass
                elif noise_value >= -1 and noise_value <= -0.7:
                    tile_type = 4 #cliff
                    
                surf = random.choice(self.terrain[TILE_TYPE[tile_type]])

                tile = Tile(tile_type, (col * TILE_SIZE, row * TILE_SIZE), surf, self.all_sprites)
                self.grid[row][col].append(tile)

    def run(self, dt):
        self.display_surface.fill('white')
        self.all_sprites.draw()
        self.input()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll forward
                    self.all_sprites.scale += 0.1
                    self.all_sprites.scale_world()
                elif event.button == 5:  # scroll backward
                    self.all_sprites.scale -= 0.1
                    if self.all_sprites.scale < 0.1:
                        self.all_sprites.scale = 0.1
                        return
                    self.all_sprites.scale_world()

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.world_surf = pygame.Surface((20000, 20000))
        self.world_rect = self.world_surf.get_rect()
        self.scaled_world = self.world_surf
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.scale = 1.0
        self.cam_step = 20
    
    def draw(self):
        mouse = pygame.mouse.get_pos()
        if mouse[1] == 0:
            self.offset.y -= self.cam_step
        elif mouse[1] >= SCREEN_HEIGHT - 1:
            self.offset.y += self.cam_step

        if mouse[0] == 0:
            self.offset.x -= self.cam_step
        elif mouse[0] >= SCREEN_WIDTH - 1:
            self.offset.x += self.cam_step

        # limit camera movement to the world scale
        self.offset.x = max(0, self.offset.x)
        self.offset.y = max(0, self.offset.y)
        self.offset.x = min(self.offset.x, self.scaled_world.get_width() - SCREEN_WIDTH)
        self.offset.y = min(self.offset.y, self.scaled_world.get_height() - SCREEN_HEIGHT)
        self.display_surface.blit(self.scaled_world, self.world_rect, self.world_rect.move(self.offset))

    def update_world(self):
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #sorted by y-axis
                if sprite.z == layer:
                    self.world_surf.blit(sprite.image, sprite.rect)
        pygame.display.flip()
    
    def scale_world(self):
        width = self.world_surf.get_width()
        height = self.world_surf.get_height()

        self.scaled_world = pygame.transform.scale(self.world_surf, (int(width * self.scale), int(height * self.scale)))
