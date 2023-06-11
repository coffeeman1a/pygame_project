import pygame, sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from world import World

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption('MiniWorld')         
		self.clock = pygame.time.Clock()
		self.world = World()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick(60) / 1000
			self.world.run(dt)
			pygame.display.update()

if __name__ == '__main__': 
	game = Game()
	game.run()