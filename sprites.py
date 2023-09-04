import pygame
from settings import *
from settings import LAYERS
from support import import_folder, import_folder_dict
import random

class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.group = groups
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

class Tile(Generic):
	def __init__(self, type ,pos, surf, groups, z=LAYERS['main']):
		super().__init__(pos, surf, groups, z)
		self.type = type
		self.z = LAYERS[TILE_TYPE[self.type]]

		self.animatiom_frame = 0

# class Civilian(pygame.sprite.Sprite):
# 	def __init__(self, pos, groups, z=LAYERS['main']):
# 		super().__init__(groups)
# 		self.setup()
# 		self.type = 'civilian'
# 		self.pos = pos
# 		self.speed = 10

# 		self.state = 'down_idle' # by default
# 		self.animation_frame = 0
# 		self.direction = pygame.math.Vector2(0,0)
# 		self.image = self.animations[self.state][self.animation_frame]

# 		self.rect = self.image.get_rect(midbottom = pos)
# 		self.hitbox = self.rect.copy().inflate((-126,-70))
# 		self.z = LAYERS_TO_RENDER[self.type]

# 		self.scale = 1


# 	def setup(self):
# 		self.animations = {'up': [],'down': [],'right': [],'left': [],
# 		     'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}
	
# 		for animation in self.animations.keys():
# 			full_path = 'sprites/civilian/' + animation
# 			self.animations[animation] = import_folder(full_path)
		
	
# 	def animate(self, dt):
		
# 		self.animation_frame += 4 * dt
		
# 		if self.animation_frame >= len(self.animations[self.state]):
# 			self.animation_frame = 0

# 		self.image = self.animations[self.state][int(self.animation_frame)]

# 		if self.direction.x > 0 and self.direction.y == 0:
# 			self.state = "right"
# 		elif self.direction.x < 0 and self.direction.y == 0:
# 			self.state = "left"

# 		if self.direction.y < 0:
# 			self.state = "up"
# 		elif self.direction.y > 0:
# 			self.state = "down"
	
# 	def get_state(self):
# 		#idle
# 		if self.direction.magnitude() == 0:
# 			self.state = self.state.split('_')[0] + '_idle'
	
# 	def move(self, dt):

# 		#normilizing a vector
# 		if self.direction.magnitude() > 0:
# 			self.direction = self.direction.normalize()

		
# 		#horizontal movement
# 		self.pos.x += self.direction.x * self.speed * dt
# 		self.hitbox.centerx = round(self.pos.x * self.scale)
# 		self.rect.centerx = self.hitbox.centerx
# 		# self.collision('horizontal')
        
# 		#vertical movement
# 		self.pos.y += self.direction.y * self.speed * dt
# 		self.hitbox.centery = round(self.pos.y * self.scale)
# 		self.rect.centery = self.hitbox.centery
# 		# self.collision('vertical')
	
# 	def random_direction(self):
# 		#random direction to move for some time
# 		if random.randint(1,100) == 1:
# 			self.direction = pygame.math.Vector2(random.randint(-1,1), random.randint(-1,1))
		

	
# 	# def collision(self, direction):

# 	# 	for sprite in self.collision_sprites.sprites():
# 	# 		if hasattr(sprite, 'hitbox'):
# 	# 			if sprite.hitbox.colliderect(self.hitbox):
# 	# 				if direction == 'horizontal':
# 	# 					if self.direction.x > 0: #moving right
# 	# 						self.hitbox.right = sprite.hitbox.left
# 	# 					if self.direction.x < 0: #moving left
# 	# 						self.hitbox.left = sprite.hitbox.right
# 	# 					self.rect.centerx = self.hitbox.centerx
# 	# 					self.pos.x = self.hitbox.centerx
# 	# 				if direction == 'vertical':
# 	# 					if self.direction.y > 0: #moving down
# 	# 						self.hitbox.bottom = sprite.hitbox.top
# 	# 					if self.direction.y < 0: #moving up
# 	# 						self.hitbox.top = sprite.hitbox.bottom
# 	# 					self.rect.centery = self.hitbox.centery
# 	# 					self.pos.y = self.hitbox.centery

	def scale_image(self):
		self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))

	def update(self, dt, scale):
		if self.scale != scale:
			self.scale = scale
			self.scale_image()
		self.get_state()
		self.animate(dt)
		self.move(dt)
		self.random_direction()
