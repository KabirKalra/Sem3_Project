import sys
import os
import pygame
import tcod


import constants

class struc_Tile:

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False



class obj_Actor:

    def __init__(self, x, y, name_object, animation, animation_speed = 0.5, creature = None, ai = None):
        self.x = x
        self.y = y
        self.animation = animation
        self.animation_speed = animation_speed / 1.0

        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0
        self.sprite_image = 0

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):

        is_visible = tcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:

            if len(self.animation) == 1:
                SURFACE_MAIN.blit(self.animation[0], (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))
            elif len(self.animation) > 1:

                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:

                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) - 1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                SURFACE_MAIN.blit(self.animation[self.sprite_image], 
                                (self.x * constants.CELL_WIDTH, self.y * constants.CELL_HEIGHT))
            
    def move(self, dx, dy):
        pass

class obj_Game:

    def __init__(self):

        self.current_map = map_create()
        self.message_history = []
        self.current_objects = []

class obj_Spritesheet:

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {'a':1, 'b':2, 'c':3, 'd':4,
                        'e':5, 'f':6, 'g':7, 'h':8,
                        'i':9, 'j':10, 'k':11, 'l':12,
                        'm':13, 'n':14 ,'o':15 ,'p': 16}

    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
                  scale = None):

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row*height, width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list

    def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, 
                    numsprites = 1,scale = None):

        image_list = []

        for i in range(numsprites):

            image = pygame.Surface([width, height]).convert()

            image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width+(width*i), row*height, width, height))

            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list


class comp_Creature:

    def __init__(self, name_instance, hp = 10, death_function = None):
        self.death_function = death_function
        self.owner = None
        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp

    def move(self, dx, dy):

        blocked = GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target, 3)
        if not blocked and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):

        game_message((self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!"), constants.COLOR_WHITE)
        target.creature.take_damage(damage)
    
    def take_damage(self, damage):
        self.hp -= damage
        game_message((self.name_instance + "'s health is "+ str(self.hp) + "/" + str(self.maxhp)), constants.COLOR_RED)

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

class AI_test:
    def __init__(self):
        self.owner = None

    def take_turn(self):
        self.owner.creature.move(tcod.random_get_int(0, -1 ,1), tcod.random_get_int(0 , -1, 1))

def death_monster(monster):

    game_message((monster.creature.name_instance + " is dead!"), constants.COLOR_GREY)

    monster.creature = None
    monster.ai = None

#class comp_Item:
#class comp_Containers:


def map_create():

    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH)]

    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

    map_make_fov(new_map)

    return new_map

def map_check_for_creatures(x, y, exclude_object = None):

    target = None

    if exclude_object:

        for objec in GAME.current_objects:
            if objec is not exclude_object and objec.x == x  and objec.y == y  and objec.creature :
                target = objec
            if target:
                return target

    else:
        for objec in GAME.current_objects:
            if objec.x == x  and objec.y == y  and objec.creature :
                target = objec
            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = tcod.map.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            tcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        tcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,constants.FOV_ALGO)

def draw_game():

    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    draw_map(GAME.current_map)

    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()

    pygame.display.flip()

def draw_map(map_to_draw):

    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visible = tcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path:
                    SURFACE_MAIN.blit(constants.S_WALL, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(constants.S_FLOOR, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:
                if map_to_draw[x][y].block_path:
                    SURFACE_MAIN.blit(constants.S_WALLEXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))
                else:
                    SURFACE_MAIN.blit(constants.S_FLOOREXPLORED, (x * constants.CELL_WIDTH, y * constants.CELL_HEIGHT))

def draw_debug():

    draw_text(SURFACE_MAIN, "FPS:" + str(int(CLOCK.get_fps())), (0,0), constants.COLOR_WHITE)

def draw_messages():

    if(len(GAME.message_history) <= constants.NUM_MESSAGES):
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-(constants.NUM_MESSAGES):]

    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)

    start_y = (constants.MAP_HEIGHT * constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 5

    i = 0

    for message, color in to_draw:

        message, color = to_draw[i]

        draw_text(SURFACE_MAIN, message, (0 , start_y + (i * text_height)), color, constants.COLOR_BLACK)

        i += 1

def draw_text(display_surface, text_to_display, T_coords,text_color, back_color = None):

    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)

def helper_text_objects(incoming_text, incoming_color, incoming_bg):

    if incoming_bg:
        text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        text_surface = constants.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return text_surface, text_surface.get_rect()

def helper_text_height(font):
    
    font_object = font.render('a', False, (0, 0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height

def game_main_loop():

    game_quit = False

    player_action = "No action"

    while not game_quit:

        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True
        elif player_action != "No action":
            for obj in GAME.current_objects:
                if obj.ai is not None:
                    obj.ai.take_turn()
        draw_game()

        CLOCK.tick(constants.GAME_FPS)

    pygame.quit()
    sys.exit()


def game_initialize():

    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()

    FOV_CALCULATE = True

    charsheet = obj_Spritesheet(os.path.join(constants.CONFIG_PATH, "Sprite_sheet1.png"))
    enemysheet = obj_Spritesheet(os.path.join(constants.CONFIG_PATH, "Sprite_sheet2.png"))
    A_PLAYER = charsheet.get_animation('o', 5, 16, 16, 2, (32, 32))
    A_ENEMY = enemysheet.get_animation('k', 1, 16, 16, 2, (32,32))
    creature_com1 = comp_Creature("Python")
    PLAYER = obj_Actor(1, 1, "Snake", A_PLAYER , creature=creature_com1)

    creature_com2 = comp_Creature("Crab", death_function= death_monster)
    ai_com = AI_test()
    ENEMY = obj_Actor(15, 15, "Crab", A_ENEMY, creature=creature_com2, ai=ai_com)

    GAME.current_objects = [PLAYER, ENEMY]

def game_handle_keys():
    global FOV_CALCULATE
    events_list = pygame.event.get()

    for event in events_list:

        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player moved"
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player moved"
    return "No action"

def game_message(game_msg, msg_color):

    GAME.message_history.append((game_msg, msg_color))

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
