#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####
from map import *
from helper_functions import *
import pygame
import random
import math


#### ====================================================================================================================== ####
#############                                         TOWER_CLASS                                                  #############
#### ====================================================================================================================== ####

class Tower:
    ''' Tower Class - represents a single Tower Object. '''
    # Represents common data for all towers - only loaded once, not per new Tower (Class Variable)
    tower_data = {}
    for tower in csv_loader("data/towers.csv"):
        tower_data[tower[0]] = { "sprite": tower[1], "damage": int(tower[2]), "rate_of_fire": float(tower[3]), "radius": int(tower[4]),'attack_mode': int(tower[5]),'laser_color': int(tower[6])}
    def __init__(self, tower_type, location, radius_sprite,TowerNo):
        ''' Initialization for Tower.
        Input: tower_type (string), location (tuple), radius_sprite (pygame.Surface), TowerNo (int)
        Output: A Tower Object
        '''
        self.TowerNo = TowerNo
        self.name = tower_type
        self.sprite = pygame.transform.scale(pygame.image.load(Tower.tower_data[tower_type]["sprite"]).convert_alpha(),(40,40))
        self.radius_sprite = radius_sprite
        self.radius = Tower.tower_data[tower_type]["radius"]
        self.damage = Tower.tower_data[tower_type]["damage"]
        self.attack_mode = Tower.tower_data[tower_type]["attack_mode"]
        self.rate_of_fire = Tower.tower_data[tower_type]["rate_of_fire"]
        self.location = location
        self.isClicked = False
        if Tower.tower_data[tower_type]["attack_mode"]==0:
            self.nextattack = 800
        else:
            self.nextattack = 200
        self.enemytarget ={}
        self.laser_color=Tower.tower_data[tower_type]["laser_color"]
        self.clock= pygame.time.Clock()

#### ====================================================================================================================== ####
#############                                       TOWER_FUNCTIONS                                                #############
#### ====================================================================================================================== ####

def update_tower(shop,towers, game_data,monstertimeline,settings,clicked):
    Towerplace=True
    (mX, mY) = pygame.mouse.get_pos()
    if shop.clicked_item is not None and clicked==False:  #if the player releases mouse
        col=mX// settings.tile_size[0]
        row=mY// settings.tile_size[1]
        for tower in towers:
            if (col*settings.tile_size[0],row*settings.tile_size[1])==tower.location: #examin if there is a tower in that place or the place is forbidden to build any tower
                Towerplace=False
        if shop.shop_data[shop.clicked_item]["available"] and Towerplace==True and 0<=col<shop.location[0]//settings.tile_size[0] and 0<=row<settings.window_size[1]//settings.tile_size[1]:
            game_data['TowerSumNum']+=1
            towers.append(Tower(shop.clicked_item,(col*settings.tile_size[0]-40,row*settings.tile_size[1]-40),shop.ui_data["radius_sprite"],game_data['TowerSumNum']))
            game_data['current_currency']-=shop.shop_data[shop.clicked_item]['cost']
        shop.clicked_item =None  
    for tower in towers:   #refresh the targeting dic
        tower.clock.tick(game_data['settings'].framerate)  # tick and deduct the passing time for every tower in order to calculate the fire time
        tower.nextattack-=tower.clock.get_time()
        if tower.attack_mode==0: # if it is the money reproduction tower
            if tower.nextattack<=0:  
                tower.nextattack=1/tower.rate_of_fire*1000
                game_data["current_currency"]+=tower.damage 
        else:                                          # if it is a combattower
            for enemycreeps in monstertimeline:
                if tower.attack_mode==1:                                    # deal with the Attack_Mode #1 tower  
                    if enemycreeps['exist'] and enemycreeps['disappear']==False and (enemycreeps['location'][0]-tower.location[0])**2+(enemycreeps['location'][1]-tower.location[1])**2<=tower.radius**2: #for attack mode 1 
                        if len(tower.enemytarget)==0 :                                    # if a) enemycreeps available AND b)the enemy within fire range AND c)the tower has no enemytarget
                            tower.enemytarget[enemycreeps['CreepNo']]=enemycreeps              # add the first enemy as the target of this tower
                        elif enemycreeps['CreepNo'] in tower.enemytarget.keys():             # if the enemycreeps has been target by this tower
                            tower.enemytarget[enemycreeps['CreepNo']]=enemycreeps              # sync the status the targeted enemy
                    else:
                        if enemycreeps['CreepNo'] in tower.enemytarget.keys():          # if a) enemy is beyond the fire range OR b)it has disappeared ,but in the dic of targeted enemies
                            tower.enemytarget.pop(enemycreeps['CreepNo'])                      # del the corresponding key
                    # for targetNo in tower.enemytarget:
                    #     angle=math.degrees(math.atan2(tower.enemytarget[targetNo]['location'][1]-tower.location[1],tower.enemytarget[targetNo]['location'][0]-tower.location[0]))%360
                    #     print('Tower:{},No:{}->Enemy:{},No:{} @{} Degrees. '.format(tower.name,tower.TowerNo,tower.enemytarget[targetNo]['type'].name,targetNo,int(angle))) 
                elif tower.attack_mode==2:                                    # deal with the Attack_Mode #1 tower  
                    if enemycreeps['exist'] and enemycreeps['disappear']==False and (enemycreeps['location'][0]-tower.location[0])**2+(enemycreeps['location'][1]-tower.location[1])**2<=tower.radius**2: #for attack mode 1 
                        if len(tower.enemytarget)<=1:                                    # if a) enemycreeps available AND b)the enemy within fire range AND c)the tower has no enemytarget
                            tower.enemytarget[enemycreeps['CreepNo']]=enemycreeps              # add the first enemy as the target of this tower
                        elif enemycreeps['CreepNo'] in tower.enemytarget.keys():             # if the enemycreeps has been target by this tower
                            tower.enemytarget[enemycreeps['CreepNo']]=enemycreeps              # sync the status the targeted enemy
                    else:
                        if enemycreeps['CreepNo'] in tower.enemytarget.keys():          # if a) enemy is beyond the fire range OR b)it has disappeared ,but in the dic of targeted enemies
                            tower.enemytarget.pop(enemycreeps['CreepNo'])      
                elif tower.attack_mode==9:                                    # deal with the Attack_Mode #1 tower  
                    if enemycreeps['exist'] and enemycreeps['disappear']==False and (enemycreeps['location'][0]-tower.location[0])**2+(enemycreeps['location'][1]-tower.location[1])**2<=tower.radius**2: #for attack mode 1 
             # if the enemycreeps has been target by this tower
                        tower.enemytarget[enemycreeps['CreepNo']]=enemycreeps              # sync the status the targeted enemy
                    else:
                        if enemycreeps['CreepNo'] in tower.enemytarget.keys():          # if a) enemy is beyond the fire range OR b)it has disappeared ,but in the dic of targeted enemies
                            tower.enemytarget.pop(enemycreeps['CreepNo'])      

def render_tower(tower, screen, settings):
    ''' Helper function that renders a single provided Tower.
    Input: Tower Object, screen (pygame display), Settings Object
    Output: None
    '''
    firemode=tower.laser_color
    if firemode==1:
        color=(0,0,random.randint(25,50))
    elif firemode==2:
        color=(220,220,random.randint(200,220))
    else :
        color =(0,0,random.randint(245,255))
    for CreepNo in tower.enemytarget:
        if tower.nextattack<200:
            pygame.draw.line(screen,color, (tower.location[0]+20,tower.location[1]+20),(tower.enemytarget[CreepNo]['location'][0]+25,tower.enemytarget[CreepNo]['location'][1]+25), 3)
    screen.blit(tower.sprite, tower.location)
