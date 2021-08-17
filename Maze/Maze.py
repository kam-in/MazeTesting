import pygame, time, random, math
from pygame.locals import *
pygame.display.init()
pygame.mixer.init()

# create the screen
screen_length = 288
screen_width = 224
display = pygame.display.set_mode((screen_length*2, screen_width*2))
screen = pygame.Surface((screen_length, screen_width))
pygame.display.set_caption("Crystals of Time by SmellyFrog")

spr_player = pygame.image.load("assets/cat.png").convert_alpha()
spr_tiles = pygame.image.load("assets/tiles2.png").convert_alpha() 
target_block = pygame.image.load("assets/dart.png").convert()




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
        if keys[pygame.K_DOWN] and self.y < screen_width-32:
            self.ySpeed += 0.2
        if keys[pygame.K_LEFT] and self.x > -1:
            self.xSpeed -= 0.2
        if keys[pygame.K_RIGHT] and self.x < screen_length-32:
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
            #print('player_x_y {} {} '.format(player.x, player.y))
            if player.x + 28 > self.x and player.x < self.x +28  and not self.col:
                if player.y + 28 > self.y and player.y + 28 < self.y + 16 :
                # player.y + 32 > self.y (if player wants to go down)
                    #print('down player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                    player.y = self.y - 32
                    player.ySpeed = 0
                    player.bottomCol = True
                    self.col = True
        
                elif player.y > self.y + 16 and player.y < self.y + 28:
                    #print('up player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                    player.y = self.y + 32
                    player.ySpeed = 0
                    player.topCol = True
                    self.col = True
            if player.y + 28 > self.y and player.y < self.y + 28 and not self.col:
                if player.x + 28 > self.x and player.x + 28 < self.x + 16:
                    #print('right player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                    player.x = self.x - 32 
                    player.xSpeed = 0
                    player.rightCol = True
                    self.col = True
                elif player.x > self.x + 16 and player.x < self.x + 28:
                    #print('left player_x_y {} {} self_x_y {} {}'.format(player.x, player.y, self.x, self.y))
                    player.x = self.x + 32
                    player.xSpeed = 0
                    player.leftCol = True
                    self.col = True
            self.col = False

        right_index = (round((player.x+32)/32), round(player.y / 32))
        left_index = (round((player.x-32) / 32), round(player.y / 32))
        up_index = (round(player.x / 32), round((player.y-32) / 32))
        down_index = (round(player.x / 32), round((player.y+32) / 32))
        #print('right{} left{} up{} down{}'.format(right_index, left_index, up_index, down_index))
        if (self.x // 32, self.y // 32) == right_index:
            if (self.x // 32, self.y // 32) in hidden_block_index:
                #print('right{} self_x_y {} {}'.format(right_index, self.x, self.y))
                remove.append(self)
            elif (self.x // 32, self.y // 32) == target:
                self.type = 2
                     
        if (self.x // 32, self.y // 32) == left_index:
            if (self.x // 32, self.y // 32) in hidden_block_index:
                #print('left{} self_x_y {} {}'.format(left_index, self.x, self.y))
                remove.append(self)
            elif (self.x // 32, self.y // 32) == target:
                self.type = 2

        if (self.x // 32, self.y // 32) == up_index:
            if (self.x // 32, self.y // 32) in hidden_block_index:
                #print('up{} self_x_y {} {}'.format(up_index, self.x, self.y))
                remove.append(self)
            elif (self.x // 32, self.y // 32) == target:
                self.type = 2
              

        if (self.x // 32, self.y // 32) == down_index: 
            if (self.x // 32, self.y // 32) in hidden_block_index:
                #print('down{} self_x_y {} {}'.format(down_index, self.x, self.y))
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

from Maze_map import *




player_y = 42069
player_x = 42069
room_num = 0
run = True
while run:
    ### level generation

    load = []
    remove = []
    player = Player(0, 0)
    hidden_block_index = []
    target = ()

    for i in range(len(layout[room_num])):
        for j in range(len(layout[room_num][i])):
            if layout[room_num][i][j] == "P":
                player = Player(j*32, i*32)
                load.append(player)
            if layout[room_num][i][j] == "0":
                load.append(Terrain(j*32, i*32, 0))
            if layout[room_num][i][j] == "1":
                load.append(Terrain(j*32, i*32, 1))
                hidden_block_index.append((j,i))
            if layout[room_num][i][j] == "2":
                load.append(Terrain(j*32, i*32, 1))
                target = (j,i)
           

    if player not in load and room_num not in (0, 14, 15):
        load.append(player)

    alive = True
    while run and alive:

        screen.fill((0, 0, 0))
    

        # event is your mouse movement, if press "x", quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        for obj in load:
            obj.update()
            obj.draw()
        for obj in remove:
            load.remove(obj)
        remove = []
        
        if (round(player.x / 32), round(player.y / 32)) == target:
            alive = False

        if room_num == 0 and (keys[pygame.K_SPACE] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
            room_num += 1      
            alive = False

        display.blit(pygame.transform.scale(screen, (screen_length*2, screen_width*2)),(0, 0))
        pygame.display.flip()


    if (round(player.x / 32), round(player.y / 32)) == target:
        room_num += 1
 
pygame.quit()
