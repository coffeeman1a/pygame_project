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

                for value_range, tile_code in TILE_MAPPING.items():
                    if value_range[0] < noise_value <= value_range[1]:
                        tile_type = tile_code
                        break
                    
                surf = random.choice(self.terrain[TILE_TYPE[tile_type]])

                tile = Tile(tile_type, (col * TILE_SIZE, row * TILE_SIZE), surf, self.tile_sprites, LAYERS[TILE_TYPE[tile_type]])
                self.grid[row][col] = tile

    def run(self, dt):
        self.display_surface.fill('white')
        self.all_sprites.draw()
        self.input()
        # self.all_sprites.render_sprites()

    def input(self):
        self.scale_map()
        # self.camera_movement()

    def scale_map(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    scale_add = 0.1 if event.button == 4 else -0.1
                    self.all_sprites.set_scale(scale_add)


    # def camera_movement(self):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_w]:
    #         self.all_sprites.offset.y -= self.all_sprites.cam_step * 10
    #     elif keys[pygame.K_s]:
    #         self.all_sprites.offset.y += self.all_sprites.cam_step * 10

    #     if keys[pygame.K_a]:
    #         self.all_sprites.offset.x -= self.all_sprites.cam_step * 10
    #     elif keys[pygame.K_d]:
    #         self.all_sprites.offset.x += self.all_sprites.cam_step * 10

class CameraGroup(pygame.sprite.Group):
    def __init__(self, tile_sprites, world_size):
        super().__init__()
        self.world_size = world_size
        self.world_width, self.world_height = WORLD_SIZE[world_size][0] * 64, WORLD_SIZE[world_size][1] * 64

        self.world_surf = pygame.Surface((self.world_width, self.world_height))
        self.world_rect = self.world_surf.get_rect()

        self.scaled_world = self.world_surf
        self.scaled_world_vector = pygame.math.Vector2(self.world_width, self.world_height)
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.scale = 1.0
        self.cam_step = 50
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.tile_sprites = tile_sprites
    
    def set_scale(self, scale_add=0) -> None:
        self.scale += scale_add

        if self.scale < SCALE_LIMITS[self.world_size]:
            self.scale = SCALE_LIMITS[self.world_size]
        
        # scaled surface 
        self.scaled_world = pygame.transform.scale(self.world_surf, self.scaled_world_vector * self.scale)
        self.scaled_rect = self.scaled_world.get_rect()

    def draw(self):
        mouse = pygame.mouse.get_pos()
        if mouse[1] == 0 or mouse[1] >= SCREEN_HEIGHT - 1 or \
            mouse[0] == 0 or mouse[0] >= SCREEN_WIDTH - 1:

            if mouse[1] == 0:
                self.offset.y -= self.cam_step * self.scale
            elif mouse[1] >= SCREEN_HEIGHT - 1:
                self.offset.y += self.cam_step * self.scale

            if mouse[0] == 0:
                self.offset.x -= self.cam_step * self.scale
            elif mouse[0] >= SCREEN_WIDTH - 1:
                self.offset.x += self.cam_step * self.scale

        self.limit_camera_movement()

        self.display_surface.blit(self.scaled_world, self.scaled_rect, self.world_rect.move(self.offset))

    def limit_camera_movement(self) -> None:
        self.offset.x = max(0, self.offset.x)
        self.offset.y = max(0, self.offset.y)
        self.offset.x = min(self.offset.x, self.scaled_world.get_width() - SCREEN_WIDTH)
        self.offset.y = min(self.offset.y, self.scaled_world.get_height() - SCREEN_HEIGHT)

    def update_world(self):
        for layer in LAYERS.values():
            for sprite in sorted(self.tile_sprites, key = lambda sprite: sprite.rect.centery): #sorted by y-axis
                if sprite.z == layer:
                    self.world_surf.blit(sprite.image, sprite.rect)
                    
        pygame.image.save(self.world_surf, "world_surf.png")
        self.world_image = pygame.image.load("world_surf.png")
        self.set_scale()
    
    # def custom_draw(self):
    #     self.world_surf.fill((0,0,0))

    #     # background image
    #     self.world_surf.blit(self.world_image, self.world_image.get_rect())
        
    #     # for active elements
    #     for layer in LAYERS.values():
    #         for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
    #             if sprite.z == layer:
    #                 self.world_surf.blit(sprite.image, sprite.rect)
