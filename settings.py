
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

TILE_SIZE = 64

LAYERS = {
    'water': 0,
    'shallow_water': 1,
	'sand': 2,
	'grass' : 3,
	'soil' : 4,
	'water soil' : 5,
	'cliff' : 6,
	'main' : 7,
	'house top' : 8,
	'fruit' : 9,
	'rain drops' : 10,
	'UI': 11
}

LAYERS_TO_RENDER = {
    'civilian' : 6
}

TILE_TYPE = {
    0: 'grass',
    1: 'shore',
    2: 'sand',
    3: 'water',
    4: 'cliff'
}

WORLD_SIZE = {
    'small': (65, 65),
    'medium': (129, 129),
    'large': (257, 257)
}

SCALE_LIMITS = {
    'small': 0.5,
    'medium': 0.3,
    'large': 0.2
}

TILE_MAPPING = {
    (0.5, 0.8): 3,   # shore
    (0.45, 0.5): 2,  # sand
    (-0.7, 0.45): 0, # grass
    (-1, -0.7): 4    # cliff
}