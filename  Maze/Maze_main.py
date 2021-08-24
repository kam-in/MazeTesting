import os

import numpy as np
import pygame
import time
import random

from psychopy import gui, event, core

from Maze_map import *


### Set specific paths --- change based on computer --- follow same folder format
filedir = '/Users/kaminkim/Documents/projects/iEEG_MAZE/MazeTesting/solving_log_dir/'#provide output file directory

### Session information GUI
correctSubj = False
while not correctSubj:
    dialog = gui.Dlg(title="") #task title ("Sherlock Spacebar Task)
    dialog.addField("Participant Number:")
    dialog.show()
    if gui.OK:
        if dialog.data[0][1].isdigit():
            subjectID = int(dialog.data[0])
            correctSubj = True

# Create the logfile
if os.path.isfile(filedir+"%d_maze_log.txt" %(subjectID)):
    os.rename(filedir+"%d_maze_log.txt" %(subjectID), filedir+"%d_maze_log_old_%s.txt" %(subjectID,time.time()))
logfile = open(filedir+"%d_maze_log.txt" %(subjectID),'w')

# Set up a global clock for keeping time
globalClock = core.Clock()

# define experiment structure
nBlock = 2
nTrial = 3

###################### START: modification of Maze.py ###########################################
# create the screen
screen_length = 288
screen_width = 224
screen = pygame.Surface((screen_length, screen_width))

def run_trial(display, screen, trial_map, spr_player, spr_tiles, target_block):

    # class Player(pygame.sprite.Sprite):
    class Player():
        def __init__(self, x, y):
            # super(Player, self).__init__()
            self.x = x
            self.y = y
            self.xSpeed = 0
            self.ySpeed = 0
            self.bottomCol = False
            self.topCol = False
            self.leftCol = False
            self.rightCol = False

        def update(self):

            self.x += self.xSpeed
            self.y += self.ySpeed

            if self.ySpeed < 8:
                self.ySpeed += 0.5
            if self.bottomCol:
                self.ySpeed = 0
                if self.xSpeed > 0:
                    self.xSpeed -= 0.3
                elif self.xSpeed < 0:
                    self.xSpeed += 0.3
                if abs(self.xSpeed) < 0.3:
                    self.xSpeed = 0

            if keys[pygame.K_UP] and self.y > -1:
                self.ySpeed -= 0.2
            if keys[pygame.K_DOWN] and self.y < screen_width - 32:
                self.ySpeed += 0.2
            if keys[pygame.K_LEFT] and self.x > -1:
                self.xSpeed -= 0.2
            if keys[pygame.K_RIGHT] and self.x < screen_length - 32:
                self.xSpeed += 0.2

        def draw(self):
            screen.blit(spr_player, (int(self.x), int(self.y)))
            # pygame.draw.rect(display, (0,255, 0), (int(self.x), int(self.y), 32, 32))


    class Terrain():
        def __init__(self, x, y, Type):
            self.x = x
            self.y = y
            self.col = False
            self.type = Type

        def update(self):

            if (self.x // 32, self.y // 32) != target:
                # print('player_x_y {} {} '.format(player.x, player.y))
                if player.x + 28 > self.x and player.x < self.x + 28 and not self.col:
                    if player.y + 28 > self.y and player.y + 28 < self.y + 16:
                        # player.y + 32 > self.y (if player wants to go down)
                        # print('down player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                        player.y = self.y - 32
                        player.ySpeed = 0
                        player.bottomCol = True
                        self.col = True

                    elif player.y > self.y + 16 and player.y < self.y + 28:
                        # print('up player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                        player.y = self.y + 32
                        player.ySpeed = 0
                        player.topCol = True
                        self.col = True
                if player.y + 28 > self.y and player.y < self.y + 28 and not self.col:
                    if player.x + 28 > self.x and player.x + 28 < self.x + 16:
                        # print('right player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                        player.x = self.x - 32
                        player.xSpeed = 0
                        player.rightCol = True
                        self.col = True
                    elif player.x > self.x + 16 and player.x < self.x + 28:
                        # print('left player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                        player.x = self.x + 32
                        player.xSpeed = 0
                        player.leftCol = True
                        self.col = True
                self.col = False

            right_index = (round((player.x + 32) / 32), round(player.y / 32))
            left_index = (round((player.x - 32) / 32), round(player.y / 32))
            up_index = (round(player.x / 32), round((player.y - 32) / 32))
            down_index = (round(player.x / 32), round((player.y + 32) / 32))
            # print('right{} left{} up{} down{}'.format(right_index, left_index, up_index, down_index))
            if (self.x // 32, self.y // 32) == right_index:
                if (self.x // 32, self.y // 32) in hidden_block_index:
                    # print('right{} self_x_y {} {}'.format(right_index, self.x, self.y))
                    remove.append(self)
                elif (self.x // 32, self.y // 32) == target:
                    self.type = 2

            if (self.x // 32, self.y // 32) == left_index:
                if (self.x // 32, self.y // 32) in hidden_block_index:
                    # print('left{} self_x_y {} {}'.format(left_index, self.x, self.y))
                    remove.append(self)
                elif (self.x // 32, self.y // 32) == target:
                    self.type = 2

            if (self.x // 32, self.y // 32) == up_index:
                if (self.x // 32, self.y // 32) in hidden_block_index:
                    # print('up{} self_x_y {} {}'.format(up_index, self.x, self.y))
                    remove.append(self)
                elif (self.x // 32, self.y // 32) == target:
                    self.type = 2

            if (self.x // 32, self.y // 32) == down_index:
                if (self.x // 32, self.y // 32) in hidden_block_index:
                    # print('down{} self_x_y {} {}'.format(down_index, self.x, self.y))
                    remove.append(self)
                elif (self.x // 32, self.y // 32) == target:
                    self.type = 2

        def draw(self):
            # this blits the tiles at the position, but starting with 6*32 end ending 32 further
            screen.blit(spr_tiles, (int(self.x), int(self.y)), (self.type * 32, 0, 32, 32))


    '''
    P is the player
    0 is the grass
    2 is the wall
    1 is the dirt
    C diamond
    4 jumper
    3 danger stone
    '''

    load = []
    remove = []
    player = Player(0, 0)
    hidden_block_index = []
    target = ()

    for i in range(len(trial_map)):
        for j in range(len(trial_map[i])):
            if trial_map[i][j] == "P":
                player = Player(j * 32, i * 32)
                load.append(player)
            if trial_map[i][j] == "0":
                load.append(Terrain(j * 32, i * 32, 0))
            if trial_map[i][j] == "1":
                load.append(Terrain(j * 32, i * 32, 1))
                hidden_block_index.append((j, i))
            if trial_map[i][j] == "2":
                load.append(Terrain(j * 32, i * 32, 1))
                target = (j, i)

    if player not in load and room_num not in (0, 14, 15):
        load.append(player)

    alive = True
    while alive:

        screen.fill((0, 0, 0))

        # event is your mouse movement, if press "x", quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # KK: LOG RESPONSE, AGENT LOCATION (COORDINATES INT HE MATRIX)
        # if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:

        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            load.remove(obj)
        remove = []

        if (round(player.x / 32), round(player.y / 32)) == target:
            alive = False

        display.blit(pygame.transform.scale(screen, (screen_length * 2, screen_width * 2)), (0, 0))
        pygame.display.flip()

##################### END: modification of Maze.py ###########################################

def run_guess(display, screen, trial_map, spr_player, spr_tiles, target_block):
    print('foo')
    # load & display the initial map status
    # ask where the goal would be
    # record the coordinate (from the maze matrix) of mouse click

print(len(layout))
# KK: ADD RANDOM SELECTION OF LAYOUTS TO USE

# running blocks
for i in range(nBlock):
    # KK: printings are for sanity check
    tseq = np.arange(0, nTrial, 1)
    print(tseq)
    random.shuffle(tseq)
    print(tseq)

    # set up and run each trial
    for j in range(len(tseq)):
        # define map & agent for this trial
        display = pygame.display.set_mode((screen_length * 2, screen_width * 2)) # needs to be run before pygame.image.load

        # re-select in a map-specific manner
        spr_player = pygame.image.load("assets/cat.png").convert_alpha()
        spr_tiles = pygame.image.load("assets/tiles2.png").convert_alpha()
        target_block = pygame.image.load("assets/dart.png").convert()

        trial_map = layout[tseq[j]]
        # run_guess(display, screen, trial_map, spr_player, spr_tiles, target_block)
        run_trial(display, screen, trial_map, spr_player, spr_tiles, target_block)
        pygame.quit()


