import pygame
import sys
import numpy as np
from pygame.locals import *
from Map import *
from pathlib import Path

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600

SOUND_FLAG = True

DIRECTION_ON_KEY = {
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
}

LEFT = 1
RIGHT = 3

pygame.init()
pygame.display.set_caption("push push")

FONT_15 = pygame.font.Font('./font/CookieRun Regular.otf', 15)
FONT_25 = pygame.font.Font('./font/CookieRun Regular.otf', 25)
FONT_35 = pygame.font.Font('./font/CookieRun Regular.otf', 35)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

cleared_stage_file = Path("./cleared_stage.npy")


class Ball:
    def __init__(self, positions):
        self.positions = positions
        self.image = pygame.image.load("./images/ball.png").convert_alpha()

    def draw(self):
        for position in self.positions:
            screen.blit(self.image, (7.5 + position[0]*45, 7.5 + position[1]*45))

    def collide(self, player_position, player_direction, brick_positions):
        if player_direction == 'up':
            temp = list(self.positions[self.positions.index(player_position)])
            temp[1] -= 1
            if (temp not in self.positions) and (temp not in brick_positions):
                self.positions[self.positions.index(player_position)][1] -= 1
                return 1
            else:
                return 0
        elif player_direction == 'down':
            temp = list(self.positions[self.positions.index(player_position)])
            temp[1] += 1
            if (temp not in self.positions) and (temp not in brick_positions):
                self.positions[self.positions.index(player_position)][1] += 1
                return 1
            else:
                return 0
        elif player_direction == 'left':
            temp = list(self.positions[self.positions.index(player_position)])
            temp[0] -= 1
            if (temp not in self.positions) and (temp not in brick_positions):
                self.positions[self.positions.index(player_position)][0] -= 1
                return 1
            else:
                return 0
        elif player_direction == 'right':
            temp = list(self.positions[self.positions.index(player_position)])
            temp[0] += 1
            if (temp not in self.positions) and (temp not in brick_positions):
                self.positions[self.positions.index(player_position)][0] += 1
                return 1
            else:
                return 0
            
    def go_back(self, player_position, direction, is_move):
        if is_move == True:
            if direction == 'up':
                self.positions[self.positions.index([player_position[0], player_position[1]-1])][1] += 1
            elif direction == 'down':
                self.positions[self.positions.index([player_position[0], player_position[1]+1])][1] -= 1
            elif direction == 'left':
                self.positions[self.positions.index([player_position[0]-1, player_position[1]])][0] += 1
            elif direction == 'right':
                self.positions[self.positions.index([player_position[0]+1, player_position[1]])][0] -= 1

class Brick:
    def __init__(self, positions):
        self.positions = positions
        self.image = pygame.image.load("./images/brick.png").convert_alpha()

    def draw(self):
        for position in self.positions:
            screen.blit(self.image, (7.5 + position[0]*45, 7.5 + position[1]*45))

class House:
    def __init__(self, positions):
        self.positions = positions
        self.image = pygame.image.load("./images/house.png").convert_alpha()
        self.changed_image = pygame.image.load("./images/fillhouse.png").convert_alpha()
        self.empty_house_group = positions
        self.past_fill_house_group = []
        self.fill_house_group = []
        self.past_fill_house_count = 0
        self.fill_house_count = 0

    def set_fill_house(self, house_position):
        if house_position not in self.fill_house_group:
            self.fill_house_group.append(house_position)

    def set_empty_house(self, house_position):
        if house_position not in self.empty_house_group:
            self.empty_house_group.append(house_position)

    def draw(self):
        self.fill_house_count = len(self.fill_house_group)
        for position in self.empty_house_group:
            screen.blit(self.image, (7.5 + position[0]*45, 7.5 + position[1]*45))
        for position in self.fill_house_group:
            screen.blit(self.changed_image, (7.5 + position[0]*45, 7.5 + position[1]*45))

    def play_fill_house_sound(self):
        if (self.past_fill_house_count <= self.fill_house_count) and (self.past_fill_house_group != self.fill_house_group):
            return True
        else:
            return False
        
    def house_update(self):
        self.past_fill_house_group = list(self.fill_house_group)
        self.past_fill_house_count = self.fill_house_count
        self.fill_house_group = []


class Nothing:
    def __init__(self, positions):
        self.positions = positions
        self.image = pygame.image.load("./images/nothing.png").convert_alpha()

    def draw(self):
        for position in self.positions:
            screen.blit(self.image, (7.5 + position[0]*45, 7.5 + position[1]*45))

class Player:
    def __init__(self, position):
        self.position = position
        self.image = pygame.image.load("./images/player.png").convert_alpha()
        self.direction = 'none'

    def draw(self):
        screen.blit(self.image, (7.5 + self.position[0]*45, 7.5 + self.position[1]*45))

    def move(self, direction):
        self.direction = direction
        if self.direction == 'up':
            self.position[1] -= 1
        elif self.direction == 'down':
            self.position[1] += 1
        elif self.direction == 'left':
            self.position[0] -= 1
        elif self.direction == 'right':
            self.position[0] += 1

    def go_back(self, direction):
        if direction == 'up':
            self.position[1] += 1
        elif direction == 'down':
            self.position[1] -= 1
        elif direction == 'left':
            self.position[0] += 1
        elif direction == 'right':
            self.position[0] -= 1
        
class Menu:
    def __init__(self):
        self.xmark_pos = [530, 157]
        self.xmark_size = [20, 20]
        self.sound_mark_pos = [200 , 157]
        self.sound_mark_size = [20, 20]
        self.soundoff_mark_size = [20, 20]
        self.leftarrow_pos = [200, 370]
        self.leftarrow_size = [100, 25]
        self.rightarrow_pos = [450, 370]
        self.rightarrow_size = [100, 25]
        self.helpblock_pos = [200, 405]
        self.helpblock_size = [100, 25]
        self.exitblock_pos = [450, 405]
        self.exitblock_size = [100, 25]
        self.minibox_size = [50, 40]
        self.click_count = 0

        self.naming = [[0 for j in range(5)] for i in range(10)]
        for i in range(0, 10):
            for j in range(0, 5):
                self.naming[i][j] = ("minibox"+str(10*(i+1)+(j+1)))

        self.can_playing = [[0 for j in range(5)] for i in range(10)]
                
        self.bigbox_image = pygame.image.load("./images/bigbox.png").convert_alpha()
        self.xmark_image = pygame.image.load("./images/xmark.png").convert_alpha()
        self.soundon_mark_image = pygame.image.load("./images/sound_on.png").convert_alpha()
        self.soundoff_mark_image = pygame.image.load("./images/sound_off.png").convert_alpha()
        self.smallbox_image = pygame.image.load("./images/smallbox.png").convert_alpha()
        self.arrow1_image = pygame.image.load("./images/arrow1.png").convert_alpha()
        self.arrow2_image = pygame.image.load("./images/arrow2.png").convert_alpha()
        self.helpblock_image = pygame.image.load("./images/block.png").convert_alpha()
        self.exitblock_image = pygame.image.load("./images/block.png").convert_alpha()
        self.miniblock_image = pygame.image.load("./images/miniblock.png").convert_alpha()
        self.clear_miniblock_image = pygame.image.load("./images/clear_miniblock.png").convert_alpha()

    def draw(self, block_num, cleared_stage):
        global SOUND_FLAG
        screen.blit(self.bigbox_image, (175, 150))
        screen.blit(self.smallbox_image, (200, 180))
        screen.blit(self.xmark_image, (self.xmark_pos[0], self.xmark_pos[1]))
        if SOUND_FLAG == True:
            screen.blit(self.soundon_mark_image, (self.sound_mark_pos[0], self.sound_mark_pos[1]))
        elif SOUND_FLAG == False:
            screen.blit(self.soundoff_mark_image, (self.sound_mark_pos[0], self.sound_mark_pos[1]))

        screen.blit(self.arrow1_image, (self.leftarrow_pos[0], self.leftarrow_pos[1]))
        screen.blit(self.arrow2_image, (self.rightarrow_pos[0], self.rightarrow_pos[1]))
        screen.blit(self.helpblock_image, (self.helpblock_pos[0], self.helpblock_pos[1]))
        screen.blit(self.exitblock_image, (self.exitblock_pos[0], self.exitblock_pos[1]))
        if block_num == 1 or block_num == 2 or block_num == 3:
            for j in range(0, 3):
                for i in range(0, 5):
                    temp_what_stage = str(3*(block_num-1)+(j+1)) + " - " + str(i+1)
                    miniblockstage_text = FONT_15.render(temp_what_stage, False, (0, 0, 0))
                    if cleared_stage[j+3*(block_num-1)][i] == 0:
                        screen.blit(self.miniblock_image, (220 + 65*i, 195 + 52.5*j))
                    elif cleared_stage[j+3*(block_num-1)][i] == 1:
                        screen.blit(self.clear_miniblock_image, (220 + 65*i, 195 + 52.5*j))
                    screen.blit(miniblockstage_text, (220 + 65*i + 8, 195 + 52.5*j + 8))
        elif block_num == 4:
            for i in range(0, 5):
                temp_what_stage = str(10) + " - " + str(i+1)
                miniblockstage_text = FONT_15.render(temp_what_stage, False, (0, 0, 0))
                if cleared_stage[9][i] == 0:
                    screen.blit(self.miniblock_image, (220 + 65*i, 195))
                elif cleared_stage[9][i] == 1:
                    screen.blit(self.clear_miniblock_image, (220 + 65*i, 195))
                screen.blit(miniblockstage_text, (220 + 65*i + 4, 195 + 8))
        helpblock_text = FONT_15.render("HELP", False, (0, 0, 0))
        screen.blit(helpblock_text, (230, 407))
        exitblock_text = FONT_15.render("EXIT", False, (0, 0, 0))
        screen.blit(exitblock_text, (485, 407))

    def clicking(self, down_pos, up_pos, thing):
        if thing == "xmark":
            if (down_pos[0] >= self.xmark_pos[0] and down_pos[0] <= self.xmark_pos[0] + self.xmark_size[0] and
                down_pos[1] >= self.xmark_pos[1] and down_pos[1] <= self.xmark_pos[1] + self.xmark_size[1] and
                up_pos[0] >= self.xmark_pos[0] and up_pos[0] <= self.xmark_pos[0] + self.xmark_size[0] and
                up_pos[1] >= self.xmark_pos[1] and up_pos[1] <= self.xmark_pos[1] + self.xmark_size[1]):
                return True
            else:
                return False

        elif thing == "leftarrow":
            if (down_pos[0] >= self.leftarrow_pos[0] and down_pos[0] <= self.leftarrow_pos[0] + self.leftarrow_size[0] and
                down_pos[1] >= self.leftarrow_pos[1] and down_pos[1] <= self.leftarrow_pos[1] + self.leftarrow_size[1] and
                up_pos[0] >= self.leftarrow_pos[0] and up_pos[0] <= self.leftarrow_pos[0] + self.leftarrow_size[0] and
                up_pos[1] >= self.leftarrow_pos[1] and up_pos[1] <= self.leftarrow_pos[1] + self.leftarrow_size[1]):
                return True
            else:
                return False

        elif thing == "rightarrow":
            if (down_pos[0] >= self.rightarrow_pos[0] and down_pos[0] <= self.rightarrow_pos[0] + self.rightarrow_size[0] and
                down_pos[1] >= self.rightarrow_pos[1] and down_pos[1] <= self.rightarrow_pos[1] + self.rightarrow_size[1] and
                up_pos[0] >= self.rightarrow_pos[0] and up_pos[0] <= self.rightarrow_pos[0] + self.rightarrow_size[0] and
                up_pos[1] >= self.rightarrow_pos[1] and up_pos[1] <= self.rightarrow_pos[1] + self.rightarrow_size[1]):
                return True
            else:
                return False

        elif thing == "helpblock":
            if (down_pos[0] >= self.helpblock_pos[0] and down_pos[0] <= self.helpblock_pos[0] + self.helpblock_size[0] and
                down_pos[1] >= self.helpblock_pos[1] and down_pos[1] <= self.helpblock_pos[1] + self.helpblock_size[1] and
                up_pos[0] >= self.helpblock_pos[0] and up_pos[0] <= self.helpblock_pos[0] + self.helpblock_size[0] and
                up_pos[1] >= self.helpblock_pos[1] and up_pos[1] <= self.helpblock_pos[1] + self.helpblock_size[1]):
                return True
            else:
                return False

        elif thing == "exitblock":
            if (down_pos[0] >= self.exitblock_pos[0] and down_pos[0] <= self.exitblock_pos[0] + self.exitblock_size[0] and
                down_pos[1] >= self.exitblock_pos[1] and down_pos[1] <= self.exitblock_pos[1] + self.exitblock_size[1] and
                up_pos[0] >= self.exitblock_pos[0] and up_pos[0] <= self.exitblock_pos[0] + self.exitblock_size[0] and
                up_pos[1] >= self.exitblock_pos[1] and up_pos[1] <= self.exitblock_pos[1] + self.exitblock_size[1]):
                return True
            else:
                return False

    def clicking_minibox(self, down_pos, up_pos, thing, block_num, cleared_stage):
        for j in range(0, 10):
            for i in range(0, 5):
                self.can_playing[j][i] = cleared_stage[j][i]
        for i in range(0, 10):
            self.can_playing[i][0] = 1
        for j in range(0, 10):
            for i in range(0, 5):
                if cleared_stage[j][i] == 0:
                    self.can_playing[j][i] = 1
                    break
        
        for j in range(0, 3):
            for i in range(0, 5):
                if thing == self.naming[j + 3*(block_num-1)][i]:
                    if (down_pos[0] >= 220 + 65*i and down_pos[0] <= 220 + 65*i + self.minibox_size[0] and
                        down_pos[1] >= 195 + 52.5*j and down_pos[1] <= 195 + 52.5*j + self.minibox_size[1] and
                        up_pos[0] >= 220 + 65*i and up_pos[0] <= 220 + 65*i + self.minibox_size[0] and
                        up_pos[1] >= 195 + 52.5*j and up_pos[1] <= 195 + 52.5*j + self.minibox_size[1]) and (self.can_playing[j + 3*(block_num-1)][i] == True):
                        return 1
                    else:
                        return 0

    def clicking_soundmark(self, down_pos, up_pos):
        global SOUND_FLAG
        if (down_pos[0] >= self.sound_mark_pos[0] and down_pos[0] <= self.sound_mark_pos[0] + self.sound_mark_size[0] and
            down_pos[1] >= self.sound_mark_pos[1] and down_pos[1] <= self.sound_mark_pos[1] + self.sound_mark_size[1] and
            up_pos[0] >= self.sound_mark_pos[0] and up_pos[0] <= self.sound_mark_pos[0] + self.sound_mark_size[0] and
            up_pos[1] >= self.sound_mark_pos[1] and up_pos[1] <= self.sound_mark_pos[1] + self.sound_mark_size[1]):
            return True
        else:
            return False

    def get_click_count(self):
        return self.click_count

    def add_click_count(self):
        self.click_count += 1
        if self.click_count == 2:
            self.click_count = 1

class Helpbox:
    def __init__(self):
        self.helpbox_pos = [200, 85]
        self.helpbox_size = [350, 400]
        self.xmark_pos = [520, 95]
        self.xmark_size = [20, 20]
        self.helpbox_image = pygame.image.load("./images/helpbox.png").convert_alpha()
        self.xmark_image = pygame.image.load("./images/xmark.png").convert_alpha()
        self.help_text = [0 for i in range(10)]
        self.help_text[0] = FONT_25.render("[ HELP ]", False, (0, 0, 0))
        self.help_text[1] = FONT_25.render("", False, (0, 0, 0))
        self.help_text[2] = FONT_25.render("게임방법: 플레이어를 움직여서", False, (0, 0, 0))
        self.help_text[3] = FONT_25.render("공을 밀어 모든 집안에 넣는다.", False, (0, 0, 0))
        self.help_text[4] = FONT_25.render("상하좌우 화살표: 이동", False, (0, 0, 0))
        self.help_text[5] = FONT_25.render("r: 레벨 재시작", False, (0, 0, 0))    
        self.help_text[6] = FONT_25.render("z: 행동 되돌리기", False, (0, 0, 0))
        self.help_text[7] = FONT_25.render("", False, (0, 0, 0))
        self.help_text[8] = FONT_25.render("원작 게임: Push Push", False, (0, 0, 0))
        self.help_text[9] = FONT_25.render("제작자: 이성주", False, (0, 0, 0))

    def draw(self):
        screen.blit(self.helpbox_image, (self.helpbox_pos[0], self.helpbox_pos[1]))
        screen.blit(self.xmark_image, (self.xmark_pos[0], self.xmark_pos[1]))
        for i in range(0, 10):
            screen.blit(self.help_text[i], (225, 100+35*i))

    def clicking_xmark(self, down_pos, up_pos):
        if (down_pos[0] >= self.xmark_pos[0] and down_pos[0] <= self.xmark_pos[0] + self.xmark_size[0] and
            down_pos[1] >= self.xmark_pos[1] and down_pos[1] <= self.xmark_pos[1] + self.xmark_size[1] and
            up_pos[0] >= self.xmark_pos[0] and up_pos[0] <= self.xmark_pos[0] + self.xmark_size[0] and
            up_pos[1] >= self.xmark_pos[1] and up_pos[1] <= self.xmark_pos[1] + self.xmark_size[1]):
            return True
        else:
            return False

    
class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super(Animation, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('./images/startscreen1.png'))
        self.images.append(pygame.image.load('./images/startscreen2.png'))
        self.images.append(pygame.image.load('./images/startscreen3.png'))
        self.images.append(pygame.image.load('./images/startscreen4.png'))
        self.images.append(pygame.image.load('./images/startscreen5.png'))
        self.images.append(pygame.image.load('./images/startscreen6.png'))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 585, 585)
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter == 15:
            self.counter = 0
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            

class GameBoard:
    brick_positions = []
    house_positions = []
    nothing_positions = []
    
    def __init__(self):
        self.player_move_sound = pygame.mixer.Sound("./music/player_move.wav")
        self.fill_house_sound = pygame.mixer.Sound("./music/fill_house.wav")
        self.level_clear_sound = pygame.mixer.Sound("./music/level_clear.wav")
        
        self.is_player_move = False
        self.is_ball_move = False
        self.player_moving = []
        self.ball_moving = []
        
        self.fillhouse_count = 0
        self.house_count = 0
        self.level = 11
        self.mapping = Map(11)
        self.move_number = 0
        self.is_menu_sound = True
        
        for i in range (13):
            for j in range (13):
                if self.mapping.map[i][j] == 1:
                    self.brick_positions.append([j, i])
                elif self.mapping.map[i][j] == 2:
                    self.house_positions.append([j, i])
                    self.house_count += 1
                elif self.mapping.map[i][j] == 3:
                    self.nothing_positions.append([j, i])

        self.ball = Ball(self.mapping.ball_positions)
        self.brick = Brick(self.brick_positions)
        self.house = House(self.house_positions)
        self.nothing = Nothing(self.nothing_positions)
        self.player = Player(self.mapping.player_position)

        self.stage_clear = [[0 for j in range(5)] for i in range(10)]
        if cleared_stage_file.is_file():
            self.stage_clear = np.load(r'./cleared_stage.npy')

    def setting(self):
        self.is_player_move = False
        self.is_ball_move = False
        self.player_moving = []
        self.ball_moving = []
        
        self.house_count = 0
        self.brick_positions = []
        self.house_positions = []
        self.nothing_positions = []
        self.mapping = Map(self.level)
        self.move_number = 0
        for i in range (13):
            for j in range (13):
                if self.mapping.map[i][j] == 1:
                    self.brick_positions.append([j, i])
                elif self.mapping.map[i][j] == 2:
                    self.house_positions.append([j, i])
                    self.house_count += 1
                elif self.mapping.map[i][j] == 3:
                    self.nothing_positions.append([j, i])
                    
        self.ball = Ball(self.mapping.ball_positions)
        self.brick = Brick(self.brick_positions)
        self.house = House(self.house_positions)
        self.nothing = Nothing(self.nothing_positions)
        self.player = Player(self.mapping.player_position)

    def update(self, screen):
        global SOUND_FLAG
        if self.player.position in self.ball.positions:
            if self.ball.collide(self.player.position, self.player.direction, self.brick.positions) == 0:
                self.player.go_back(self.player.direction)
                self.is_player_move = False
                self.is_ball_move = False
            else:
                self.is_player_move = True
                self.is_ball_move = True
                
        if self.player.position in self.brick.positions:
            self.player.go_back(self.player.direction)
            self.is_player_move = False

        self.nothing.draw()
        self.brick.draw()
        self.ball.draw()
      
        for house_pos in self.house.positions:
            if house_pos in self.ball.positions:
                self.house.set_fill_house(house_pos)
            else:
                self.house.set_empty_house(house_pos)
        self.house.draw()
        self.house_sound_flag = self.house.play_fill_house_sound()
        self.house.house_update()
        self.player.draw()

        if self.is_player_move == True:
            if self.is_menu_sound == True: 
                pygame.mixer.stop()
                self.is_menu_sound = False
            if (self.house_sound_flag == False) and (SOUND_FLAG == True):
                pygame.mixer.Sound.play(self.player_move_sound)
            elif (self.house_sound_flag == True) and (SOUND_FLAG == True):
                pygame.mixer.Sound.play(self.fill_house_sound)
            self.move_number += 1
            if self.move_number == 1000:
                self.move_number = 999
            self.player_moving.append(self.player.direction)
            self.ball_moving.append(self.is_ball_move)
            if len(self.player_moving) > 3:
                del self.player_moving[0]
            if len(self.ball_moving) > 3:
                del self.ball_moving[0]
        
        self.is_player_move = False
        self.is_ball_move = False


    def level_clear(self):
        global SOUND_FLAG
        if self.house.fill_house_count == self.house_count:
            self.stage_clear[(self.level//10)-1][(self.level%10)-1] = 1
            self.level += 1
            if self.level == 106:
                self.level = 105
            if self.level % 10 == 6:
                self.level += 5
            self.setting()
            if SOUND_FLAG == True:
                pygame.mixer.Sound.play(self.level_clear_sound)
            cleared_stage = np.array(self.stage_clear)
            #np.save(r'C:\Users\spdlq\AppData\Local\Programs\Python\Python37-32\cleared_stage', cleared_stage)
            np.save(r'./cleared_stage', cleared_stage)
        

    def setting_level(self, level):
        self.level = level
        self.setting()
    

animation_sprite = Animation()
animation_group = pygame.sprite.Group(animation_sprite)
game_board = GameBoard()
menu = Menu()
helpbox = Helpbox()

menu_event = False
xmark_event = False
soundmark_event = False
leftarrow_event = False
rightarrow_event = False
helpblock_event = False
exitblock_event = False
minibox_event = [[0 for j in range(5)] for i in range(10)]
helpbox_xmark_event = False

background_sound = pygame.mixer.Sound("./music/background.wav")
pygame.mixer.Sound.play(background_sound)

mousebuttondown_event = False
mousebuttonup_event = False
mousebuttondown_position = (-10, -10)
mousebuttonup_position = (-10, -10)

block_number = 1

while True:
    menu_click_count = menu.get_click_count()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (event.type == pygame.KEYDOWN) and (menu_event == False) and (menu_click_count != 0):
            if event.key in DIRECTION_ON_KEY:
                game_board.player.move(DIRECTION_ON_KEY[event.key])
                game_board.is_player_move = True
                game_board.update(screen)
            elif event.key == ord('z'):
                if len(game_board.player_moving) > 0:
                    direction = game_board.player_moving.pop()
                    game_board.ball.go_back(game_board.player.position, direction, game_board.ball_moving.pop())
                    game_board.player.go_back(direction)
            elif event.key == ord('r'):
                game_board.setting()
        if event.type == MOUSEBUTTONDOWN and event.button == LEFT:
            mousebuttondown_event = True
            mousebuttondown_position = event.pos
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
            mousebuttonup_event = True
            mousebuttonup_position = event.pos
        if (mousebuttondown_event == True) and (mousebuttonup_event == True):
            mousebuttondown_event = False
            mousebuttonup_event = False
    if (mousebuttondown_position[0] >= 610 and mousebuttondown_position[0] <= 730 and
        mousebuttondown_position[1] >= 7.5 and mousebuttondown_position[1] <= 87.5 and
        mousebuttonup_position[0] >= 610 and mousebuttonup_position[0] <= 730 and
        mousebuttonup_position[1] >= 7.5 and mousebuttonup_position[1] <= 87.5):
        menu_event = True

    if menu_event == True:
        xmark_event = menu.clicking(mousebuttondown_position, mousebuttonup_position, "xmark")
        leftarrow_event = menu.clicking(mousebuttondown_position, mousebuttonup_position, "leftarrow")
        rightarrow_event = menu.clicking(mousebuttondown_position, mousebuttonup_position, "rightarrow")
        if helpblock_event == False:
            helpblock_event = menu.clicking(mousebuttondown_position, mousebuttonup_position, "helpblock")
        exitblock_event = menu.clicking(mousebuttondown_position, mousebuttonup_position, "exitblock")
        soundmark_event = menu.clicking_soundmark(mousebuttondown_position, mousebuttonup_position)
       
        if block_number == 1:
            for i in range(0, 3):
                for j in range(0, 5):
                    minibox_event[i][j] = menu.clicking_minibox(mousebuttondown_position, mousebuttonup_position, menu.naming[i][j], block_number, game_board.stage_clear)
        elif block_number == 2:
            for i in range(3, 6):
                for j in range(0, 5):
                    minibox_event[i][j] = menu.clicking_minibox(mousebuttondown_position, mousebuttonup_position, menu.naming[i][j], block_number, game_board.stage_clear)
        elif block_number == 3:
            for i in range(6, 9):
                for j in range(0, 5):
                    minibox_event[i][j] = menu.clicking_minibox(mousebuttondown_position, mousebuttonup_position, menu.naming[i][j], block_number, game_board.stage_clear)
        elif block_number == 4:
            for i in range(9, 10):
                for j in range(0, 5):
                    minibox_event[i][j] = menu.clicking_minibox(mousebuttondown_position, mousebuttonup_position, menu.naming[i][j], block_number, game_board.stage_clear)
    
    background_image = pygame.image.load("./images/background.png").convert_alpha()
    screen.blit(background_image, (0, 0))
    board_image = pygame.image.load("./images/board.png").convert_alpha()
    screen.blit(board_image, (7.5, 7.5)) #(45*13 = 585)
    
    menubar_image = pygame.image.load("./images/menubar.png").convert_alpha()
    screen.blit(menubar_image, (610, 7.5))

    stagestepbox_image = pygame.image.load("./images/stagestepbox.png").convert_alpha()
    screen.blit(stagestepbox_image, (610, 107.5))

    stageblock_text = FONT_25.render("stage", False, (0, 0, 0))
    screen.blit(stageblock_text, (638, 125))
    stepblock_text = FONT_25.render("step", False, (0, 0, 0))
    screen.blit(stepblock_text, (643, 358))
    what_stage = [1, 1]
    what_stage[0] = game_board.level // 10
    what_stage[1] = game_board.level % 10
    stage_string = str(what_stage[0]) + " - " + str(what_stage[1])
    stage_text = FONT_35.render(stage_string, False, (0, 0, 0))
    if what_stage[0] == 10:
        screen.blit(stage_text, (623, 230))
    else:
        screen.blit(stage_text, (632, 230))
    what_step = game_board.move_number
    step_string = str(what_step)
    step_text = FONT_35.render(step_string, False, (0, 0, 0))
    if what_step < 10:
        screen.blit(step_text, (660, 450))
    elif what_step >= 10 and what_step < 100:
        screen.blit(step_text, (650, 450))
    elif what_step >= 100:
        screen.blit(step_text, (640, 450))

    game_board.update(screen)

    if menu_click_count == 0:
        animation_group.update()
        animation_group.draw(screen)

    if menu_event == True:
        menu.draw(block_number, game_board.stage_clear)

    if helpblock_event == True:
        helpbox.draw()
        helpbox_xmark_event = helpbox.clicking_xmark(mousebuttondown_position, mousebuttonup_position)
        if helpbox_xmark_event == True:
            helpbox_xmark_event = False
            helpblock_event = False
        pygame.display.flip()
        continue
    
    if xmark_event == True:
        xmark_event = False
        menu_event = False

    if soundmark_event == True:
        soundmark_event = False
        if SOUND_FLAG == True:
            SOUND_FLAG = False
            if menu_click_count == 0:
                pygame.mixer.pause()
            else:
                pygame.mixer.stop()
        elif SOUND_FLAG == False:
            SOUND_FLAG = True
            pygame.mixer.unpause()
        mousebuttondown_position = (-10, -10)
        mousebuttonup_position = (-10, -10)

    if leftarrow_event == True:
        block_number -= 1
        if block_number < 1:
            block_number = 1
        leftarrow_event = False
        mousebuttondown_position = (-10, -10)
        mousebuttonup_position = (-10, -10)
        
    if rightarrow_event == True:
        block_number += 1
        if block_number > 4:
            block_number = 4
        rightarrow_event = False
        mousebuttondown_position = (-10, -10)
        mousebuttonup_position = (-10, -10)

    if block_number == 1:
        for i in range(0, 3):
            for j in range(0, 5):
                if minibox_event[i][j] == 1:
                    menu.add_click_count()
                    minibox_event[i][j] = 0
                    mousebuttondown_position = (-10, -10)
                    mousebuttonup_position = (-10, -10)
                    game_board.setting_level(10*(i+1)+(j+1))
    elif block_number == 2:
        for i in range(3, 6):
            for j in range(0, 5):
                if minibox_event[i][j] == 1:
                    menu.add_click_count()
                    minibox_event[i][j] = 0
                    mousebuttondown_position = (-10, -10)
                    mousebuttonup_position = (-10, -10)
                    game_board.setting_level(10*(i+1)+(j+1))
    elif block_number == 3:
        for i in range(6, 9):
            for j in range(0, 5):
                if minibox_event[i][j] == 1:
                    menu.add_click_count()
                    minibox_event[i][j] = 0
                    mousebuttondown_position = (-10, -10)
                    mousebuttonup_position = (-10, -10)
                    game_board.setting_level(10*(i+1)+(j+1))
    elif block_number == 4:
        for i in range(9, 10):
            for j in range(0, 5):
                if minibox_event[i][j] == 1:
                    menu.add_click_count()
                    minibox_event[i][j] = 0
                    mousebuttondown_position = (-10, -10)
                    mousebuttonup_position = (-10, -10)
                    game_board.setting_level(10*(i+1)+(j+1))

    if exitblock_event == True:
        exitblock_event = False
        pygame.quit()
        sys.exit()
        
    pygame.display.flip()
    game_board.level_clear()

    
