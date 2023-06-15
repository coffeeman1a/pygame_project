
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

TILE_SIZE = 64

LAYERS = {
    'water': 0,
	'sand': 1,
	'grass' : 2,
	'soil' : 3,
	'water soil' : 4,
	'cliff' : 5,
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
    'pocket': (65, 65),
    'small': (129, 129),
    'medium': (257, 257),
    'large': (513, 513),
    'huge': (1025, 1025)
}