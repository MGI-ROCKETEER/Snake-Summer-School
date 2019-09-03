#Snake Tutorial Python
#import RPi.GPIO as gpio

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
"""
button1 = 18
button2 = 23
button3 = 24
button4 = 25
gpio.setmode(gpio.BCM)

gpio.setup(button1, gpio.IN)
gpio.setup(button2, gpio.IN)
gpio.setup(button3, gpio.IN)
gpio.setup(button4, gpio.IN)
"""
WHITE_COLOR = (255, 255, 255) # Color for score display
pygame.font.init()
font = pygame.font.SysFont('comicsans', 30)
width = 500
rows = 20
score = 0
win = pygame.display.set_mode((width, width))
import pygame
import sys
from pygame.locals import *

if not pygame.font.get_init():
    pygame.font.init()


class Menu(object):
    ''' Simple class designed for drawing menus.
        The simplest way to initialize this menu in your program is to call these three lines:
        menu = Menu(['field1', 'field2', 'field3', 'Exit'])
        menu.init(x)  # x variable should contain screen surface, e.g. called by pygame.display.set_mode()
        menu.draw()
    '''
    curr_position = 0  # variable used for getting current highlighted field
    font_size = 60
    font_style = 'bauhaus93'
    ground_colour = (0, 0, 0)
    text_colour = (255, 255, 255)
    curr_selection_colour = (60, 200, 60)  # highlight colour

    def __init__(self, text_list):
        self.text_list = text_list
        self.fields_num = len(text_list)

    def set_colors(self, ground_color, text_colour, curr_selection):
        # allows alternative change of colour sets
        self.ground_colour = ground_color
        self.text_list = text_colour
        self.curr_selection_colour = curr_selection

    def set_fontsize(self, font_size):
        self.font_size = font_size

    def init(self, surface):
        # method for initializing font and getting surface
        # while calling this method, one should pass the variable with screen surface
        self.font = pygame.font.SysFont(self.font_style, self.font_size)
        self.surface = surface

    def draw(self, move=0):
        # responsible for checking which field should be highlighted, getting current fields positions required for drawing
        # and drawing all of the menu on screen
        self.surface.fill(self.ground_colour)
        if self.curr_position + move in range(self.fields_num):
            self.curr_position += move
        screen_size = self.surface.get_size()
        menu_height = self.font.size(self.text_list[-1])[1] * self.fields_num
        center = [screen_size[0] / 2, (screen_size[1] - menu_height) / 2]
        pos = [0, center[1]]
        for i in range(self.fields_num):
            pos[0] = center[0] - self.font.size(self.text_list[i])[0] / 2
            if i == self.curr_position:
                text = self.font.render(self.text_list[i], 1, self.curr_selection_colour)
                self.surface.blit(text, pos)
            else:
                text = self.font.render(self.text_list[i], 1, self.text_colour)
                self.surface.blit(text, pos)
            pos[1] += self.font_size * 1.2
        pygame.display.update()

    def start(self):
        # main menu loop, you can exit by pressing ESC keyboard button, by choosing EXIT field
        # or just by clicking eXit (close) button on a window
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    shutdown()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        shutdown()
                    if event.key == K_RETURN:
                        # always the last field should be Exit
                        if self.curr_position == self.fields_num - 1:
                            shutdown()
                        elif self.curr_position == 0:
                            return 2
                        elif self.curr_position == 1:
                            return 3
                    if event.key == K_UP:
                        self.draw(-1)
                    if event.key == K_DOWN:
                        self.draw(1)
        pygame.time.wait(10)


def shutdown():
    pygame.quit()
    sys.exit()
    
# if the game starts, wait some time
pygame.time.wait(1500)  

def start_screen():
    # initializing menu, getting single or multiplayer after choosing game mode
    global PLAYERS
    menu = Menu(['Let us start', 'Exit'])
    menu.init(win)
    menu.draw()
    PLAYERS = menu.start() 

class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
 
       
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
class snake(object):
    body = []
    turns = {}
    speed = 5
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.speed = 5
    
    def moverasp(self):
        if gpio.input(button1):
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        elif gpio.input(button2):
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif gpio.input(button3):
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif gpio.input(button4):
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # c is synonym for the blocks after the head of the snake
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
 
        for i, c in enumerate(self.body): # c is synonym for the blocks after the head of the snake
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
       
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.speed = 5
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack, score, dorian, dorian2,win
    win = pygame.display.set_mode((width, width))
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    dorian.draw(surface)
    dorian2.draw(surface)
    if bonus:
        bonus.draw(surface)
    drawGrid(width,rows, surface)
    
    
    text = font.render('Your score: ' + str(score), True, WHITE_COLOR)
    win.blit(text, (0, 0))
    pygame.display.update()
 
 
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)

def randomDorian(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 
def main():
    global width, rows, s, snack, score, dorian, dorian2, bonus
    width = 500
    rows = 20
    score = 0
    win = pygame.display.set_mode((width, width))
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    dorian = cube(randomDorian(rows, s), color=(225,225,225))
    dorian2 = cube(randomDorian(rows,s), color=(225,225,225))
    #bonus = cube((0,0), color=(0,0,0))
    flag = True
    bonus = False
    bonus_time = 0
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(50)
        clock.tick(s.speed)
        s.move()
        i = random.choice([0,1,2])
        c = 0
        if((s.body[0].pos == snack.pos) and (i==0)):##
            s.addCube()##
            snack = cube(randomSnack(rows, s), color = (0,225,0))
            dorian = cube(randomDorian(rows,s), color = (225,225,225))
            c = c+1
            score +=1
            s.speed = s.speed+4 #everytimeeats cube goes faster
            if score % 5 == 0 and c != 0:
                bonus = cube(randomSnack(rows, s), color=(128,0,128))    
            if len(s.body) == 5:
                s.speed = s.speed-10#if length is 4 he goes 10 slower
            if len(s.body) == 10:
                s.speed = s.speed-15
            if len(s.body) == 15:
                s.speed = s.speed-10
            if len(s.body) == 20:
                s.speed = s.speed-15
            if len(s.body) == 25:
                s.speed = s.speed-10
            if len(s.body) == 30:
                s.speed = s.speed-15
            if len(s.body) == 35:
                s.speed = s.speed-10
            if len(s.body) == 40:
                s.speed = s.speed-15
            if((c%3 == 0)):
                dorian2 = cube(randomDorian(rows,s), color =(225,225,225))
        elif((s.body[0].pos == snack.pos) and (i==1)):##
            s.addCube()##
            snack = cube(randomSnack(rows, s), color = (0,0,225))
            dorian = cube(randomDorian(rows,s), color = (225,225,225))
            c = c+1
            score +=1
            s.speed = s.speed+4
            if score % 5 == 0 and c != 0:
                bonus = cube(randomSnack(rows, s), color=(128,0,128))    #everytimeeats cube goes faster
            if len(s.body) == 5:
                s.speed = s.speed-10#if length is 4 he goes 10 slower
            if len(s.body) == 10:
                s.speed = s.speed-15
            if len(s.body) == 15:
                s.speed = s.speed-10
            if len(s.body) == 20:
                s.speed = s.speed-15
            if len(s.body) == 25:
                s.speed = s.speed-10
            if len(s.body) == 30:
                s.speed = s.speed-15
            if len(s.body) == 35:
                s.speed = s.speed-10
            if len(s.body) == 40:
                s.speed = s.speed-15
            if((c%3 == 0)):
                dorian2 = cube(randomDorian(rows,s), color =(225,225,225))
        elif((s.body[0].pos == snack.pos) and (i==2)):##
            s.addCube()##
            snack = cube(randomSnack(rows, s), color = (255,0,0))
            dorian = cube(randomDorian(rows,s), color = (225,225,225))
            c = c+1
            score +=1
            s.speed = s.speed+4
            if score % 5 == 0 and c != 0:
                bonus = cube(randomSnack(rows, s), color=(128,0,128))    #everytimeeats cube goes faster
            if len(s.body) == 5:
                s.speed = s.speed-10#if length is 4 he goes 10 slower
            if len(s.body) == 10:
                s.speed = s.speed-15
            if len(s.body) == 15:
                s.speed = s.speed-10
            if len(s.body) == 20:
                s.speed = s.speed-15
            if len(s.body) == 25:
                s.speed = s.speed-10
            if len(s.body) == 30:
                s.speed = s.speed-15
            if len(s.body) == 35:
                s.speed = s.speed-10
            if len(s.body) == 40:
                s.speed = s.speed-15
            if((c%3 == 0)):
                dorian2 = cube(randomDorian(rows,s), color =(225,225,225))
        

        elif s.body[0].pos == dorian.pos:
            print('Score: ', len(s.body))
            message_box('u crazy?!?', 'LOOK OUT man!!')
            s.reset((10,10))
            score = 0
            break

        elif bonus and s.body[0].pos == bonus.pos:
            score += 5
            bonus = False
            
        elif s.body[0].pos == dorian2.pos:
            print('Score: ', len(s.body))
            message_box('u crazy?!?', 'LOOK OUT man!!')
            s.reset((10,10))
            score = 0
            break

        elif type(bonus) != bool :
            bonus_time += 1
            if bonus_time == 50:
                bonus = False
                bonus_time = 0
 
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print('Score:', len(s.body))
                message_box('ouchh', 'loooooook ouuuut!')
                s.reset((10,10))
                score = 0
                break
 
           
        redrawWindow(win)
 
       
    pass
 
start_screen()
main()
 
