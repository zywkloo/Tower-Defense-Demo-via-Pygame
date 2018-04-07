#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame
import math

#### ====================================================================================================================== ####
#############                                         ENEMY_CLASS                                                  #############
#### ====================================================================================================================== ####

class Enemy:
    ''' Enemy Class - represents a single Enemy Object. '''
    # Represents common data for all enemies - only loaded once, not per new Enemy (Class Variable)
    enemy_data = {}
    for enemy in csv_loader("data/enemies.csv"):
        enemy_data[enemy[0]] = { "sprite": enemy[1], "health": int(enemy[2]), "speed": float(enemy[3]) ,'towerdamage':int(enemy[4]),'basedamage':int(enemy[5]),'moneydrop':int(enemy[6])}
    def __init__(self, enemy_type):
        ''' Initialization for Enemy.
        Input: enemy type (string), location (tuple of ints)
        Output: An Enemy Object
        '''
        self.name = enemy_type
        self.sprite = pygame.image.load(Enemy.enemy_data[enemy_type]["sprite"])
        self.health = Enemy.enemy_data[enemy_type]["health"]
        self.speed = Enemy.enemy_data[enemy_type]["speed"]
        self.direction = None
        self.towerdamage=Enemy.enemy_data[enemy_type]["towerdamage"]
        self.basedamage=Enemy.enemy_data[enemy_type]['basedamage']
        self.moneydrop=Enemy.enemy_data[enemy_type]['moneydrop']

#### ====================================================================================================================== ####
#############                                         Gamelevel_CLASS                                              #############
#### ====================================================================================================================== ####

class Gamelevel:
    '''  Gamelevel Class - represents a single game level Object. '''
    # Represents common data for all enemies waves, show-up time and position in a certain game level- only loaded once
    level_data ={}
    for level in csv_loader("data/gamelevel.csv"):
        if int(level[0]) not in level_data.keys():
            level_data[int(level[0])]=[]
            CreepNo=1
        level_data[int(level[0])].append({'CreepNo':CreepNo+int(level[0])*1000,'type':Enemy(level[1]),'start_time':float(level[2]),'start_pos':min(max(int(level[3]),1),20)-1,'location':(19*40,(min(max(int(level[3]),1),20)-1)*40-9),'exist':False,'dead':False,'disappear':False,'wave':max(int(level[6]),1),'currenthp':Enemy(level[1]).health})
        CreepNo+=1
    '''
    level_data={1:[ {'CreepNo':1001,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':1002,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':1003,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health}],
                2:[ {'CreepNo':2001,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':2002,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':2003,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health}],
                3:[ {'CreepNo':3001,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':3002,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
                    {'CreepNo':3003,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health}]
                }  # each row is an $ enemycreeps $ entity

    '''
    def __init__(self, level_num):
        ''' Initialization for Enemy.
        Input: level_num, the No. of this level ( ints)
        Output: An Enemy Object
        '''
        self.name = "Level "+str(level_num)
        self.lvNo = level_num
        self.monstertimeline =Gamelevel.level_data[level_num] # a list of  dic of every enemycreep
        self.endtime = 56000
        self.clock= pygame.time.Clock()
        self.currenttime= 0
'''
Gamelevel.monstertimeline
[ {'CreepNo':1001,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
  {'CreepNo':1002,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health},
  {'CreepNo':1003,'type':Enemy('Enemytype'),'star_time':float,'start_pos':int,'location':tuple,'exist':False,'dead':False,'disappear':False,'wave':int,'currenthp':Enemy('Enemytype').health}],

'''


#### ====================================================================================================================== ####
#############                                       ENEMY_FUNCTIONS                                                #############
#### ====================================================================================================================== ####

def update_enemy(enemycreeps,gamedata,towers,damage=0):
    enemycreeps['currenthp'] -= damage    #112312313123 
    if enemycreeps['currenthp']<=0:
        enemycreeps['dead']=True
        enemycreeps['disappear']=True
        gamedata["current_currency"]+=enemycreeps['type'].moneydrop
    elif enemycreeps['location'][0]<40:
        enemycreeps['disappear']=True
        gamedata['totalhp']=max(gamedata['totalhp']-enemycreeps['type'].basedamage,0)
    else:
        enemycreeps['location']=(enemycreeps['location'][0]-enemycreeps['type'].speed,enemycreeps['location'][1])

def render_enemy(enemycreeps, screen, settings):
    ''' Helper function that renders a single provided Enemy.
    Input: Enemy Object, screen (pygame display), Settings Object
    Output: None
    '''
    screen.blit(pygame.transform.scale(enemycreeps['type'].sprite.convert_alpha(),(58,58)), enemycreeps['location'])
