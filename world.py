import pygame, random, math as m
from opensimplex import OpenSimplex
from settings import *
from sprites import Tile
from support import import_folder, import_folder_dict

class World():
    def __init__(self) -> None:
        self.world_size = input('Enter world size: ')
        self.display_surface = pygame.display.get_surface()
        self.tile_sprites = pygame.sprite.Group()
        self.all_sprites = CameraGroup(self.tile_sprites, self.world_size)

        # terrain
        self.terrain = {}

        # noise parameters
        self.seed = random.randint(0, 100)
        self.noise = OpenSimplex(self.seed)
        self.noise_map = []
        self.civ = None
        self.setup()

    def setup(self):
        
        for tile_id, tile_name in TILE_TYPE.items():
            self.terrain[tile_name] = import_folder(f'sprites/terrain/{tile_name}')
        
        self.generate_world(WORLD_SIZE[self.world_size])
        self.all_sprites.update_world()

    def generate_world(self, world_size):

        width = world_size[0]
        height = world_size[1]
        scale = 64
        h_tiles, v_tiles = width, height
        self.grid = [[[] for col in range (h_tiles)] for row in range(v_tiles)]

        noise = OpenSimplex(random.randint(0, 100))

        # generate tiles in square grid
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
                self.grid[row][col] = tile
        #self.civ = Civilian(pygame.math.Vector2(500,500), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('white')
        self.all_sprites.draw()
        self.input()
        #self.civ.update(dt)
        #self.all_sprites.render_sprites()

    def input(self):
        self.scale_map()

    def scale_map(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll forward
                    self.all_sprites.scale += 0.1
                elif event.button == 5:  # scroll backward
                    self.all_sprites.scale -= 0.1
                    if self.all_sprites.scale < 0.1:
                        self.all_sprites.scale = 0.1
                        return
                self.all_sprites.scale_world()

class CameraGroup(pygame.sprite.Group):
    def __init__(self, tile_sprites, world_size):
        super().__init__()
        self.world_size = world_size
        self.world_width, self.world_height = WORLD_SIZE[world_size][0] * 64, WORLD_SIZE[world_size][1] * 64
        self.world_surf = pygame.Surface((self.world_width, self.world_height))
        self.world_rect = self.world_surf.get_rect()
        self.scaled_world = self.world_surf
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.scale = 1.0
        self.cam_step = 20
        self.tile_sprites = tile_sprites
    
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
        self.world_surf.fill((0, 0, 0))
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): #sorted by y-axis
                if sprite.z == layer:
                    self.world_surf.blit(sprite.image, sprite.rect)
                    
        pygame.image.save(self.world_surf, "world_surf.png")
        self.world_image = pygame.image.load("world_surf.png")
        pygame.display.flip()
    
    def render_sprites(self):
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    self.world.blit(sprite.image, sprite.rect.move(self.offset))
        pygame.display.flip()

    def scale_world(self):
        width = self.world_image.get_width()
        height = self.world_image.get_height()
        
        if self.scale < SCALE_LIMITS[self.world_size]:
            self.scale = SCALE_LIMITS[self.world_size]

        print(self.scale)
        self.scaled_world = pygame.transform.scale(self.world_image, (int(width * self.scale), int(height * self.scale)))
