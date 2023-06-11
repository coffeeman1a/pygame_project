import pygame
from settings import LAYERS
from support import import_folder, import_folder_dict

class WorldSurface(pygame.surface.Surface):
	def __init_subclass__(cls, rect) -> None:
		self.rect = rect
		return super().__init_subclass__()


class Generic(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = LAYERS['main']):
		super().__init__(groups)
		self.image = surf
		self.rect = self.image.get_rect(topleft = pos)
		self.z = z
		self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)


class Tile(Generic):
	def __init__(self, type ,pos, surf, groups, z=LAYERS['main']):
		super().__init__(pos, surf, groups, z)
		self.type = type
