import os
import pygame
import tcod
pygame.init()

#Game dimensions
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

#FPS limit

GAME_FPS = 60

#Map dimensions

MAP_WIDTH = 20
MAP_HEIGHT = 20

#Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)

#Game colors
COLOR_DEFAULT_BG = COLOR_GREY

#Sprites
ROOT_DIR = os.getcwd()
CONFIG_PATH = os.path.join(ROOT_DIR, "Sprites\\")
#S_PLAYER = pygame.image.load(os.path.join(constants.CONFIG_PATH, "Main_character.png"))
#S_ENEMY = pygame.image.load(os.path.join(constants.CONFIG_PATH, "Enemy_1.png"))
S_WALL = pygame.image.load(os.path.join(CONFIG_PATH, "Wall_v2.png"))
S_WALLEXPLORED = pygame.image.load(os.path.join(CONFIG_PATH, "Wall_v4.png"))
S_FLOOR = pygame.image.load(os.path.join(CONFIG_PATH, "Floor_1.jpeg"))
S_FLOOREXPLORED = pygame.image.load(os.path.join(CONFIG_PATH, "Floor_3.jpeg"))

# FOV settings
FOV_ALGO = tcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#Fonts
FONT_DEBUG_MESSAGE = pygame.font.Font("C:\\Users\\kkalr\\Desktop\\Sprites\\joystix.ttf", 15)
FONT_MESSAGE_TEXT =  pygame.font.Font("C:\\Users\\kkalr\\Desktop\\Sprites\\joystix.ttf", 12)

#Message defaults
NUM_MESSAGES = 4
