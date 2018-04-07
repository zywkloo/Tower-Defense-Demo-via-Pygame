#Yiwei Zhang 101071022
#######
#Music website: https://www.newgrounds.com/audio/listen/764823  ;Author: ET16 
#Licence https://creativecommons.org/licenses/by-nc-nd/3.0/
#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
from settings import *
from shop import *
from tower import *
from enemy import *
from map import *
import pygame
import sys
import math

#### ====================================================================================================================== ####
#############                                         INITIALIZE                                                   #############
#### ====================================================================================================================== ####

def initialize():
    ''' Initialization function - initializes various aspects of the game including settings, shop, and more.
    Input: None
    Output: game_data dictionary
    '''
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("COMP 1501 - Tutorial 7: Tower Defense (TD) Base Code")

    # Initialize the Settings Object
    settings = Settings()

    # Initialize game_data and return it
    game_data = { "screen": pygame.display.set_mode(settings.window_size),
                  "current_currency": settings.starting_currency,
                  "current_wave": 0,
                  "stay_open": 1,
                  "selected_tower": None,
                  "clicked": False,
                  "settings": settings,
                  "towers": [],
                  "shop": Shop("Space", settings),
                  "map": Map(settings),
                  'gamelevel':Gamelevel(1), #current gamelevel object
                  'nextlevel':2,     #next gamelevel int
                  'totalhp':100,
                  'TowerSumNum':0,
                  "Oversprite":pygame.transform.scale(pygame.image.load("assets/map/background.png").convert_alpha(), settings.window_size)}

    return game_data

#### ====================================================================================================================== ####
#############                                           PROCESS                                                    #############
#### ====================================================================================================================== ####

def process(game_data):
    ''' Processing function - handles all form of user input. Raises flags to trigger certain actions in Update().
    Input: game_data dictionary
    Output: None
    '''
    for event in pygame.event.get():

        # Handle [X] press
        if event.type == pygame.QUIT:
            game_data["stay_open"] = 0

        # Handle Mouse Button Down
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_data["clicked"] = True
            game_data["selected_tower"] = False

        # Handle Mouse Button Up
        if event.type == pygame.MOUSEBUTTONUP:
            game_data["clicked"] = False

#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####

def update(game_data):
    ''' Updating function - handles all the modifications to the game_data objects (other than boolean flags).
    Input: game_data
    Output: None
    '''
    
    game_data['gamelevel'].clock.tick(game_data['settings'].framerate)
    game_data['gamelevel'].currenttime+=game_data['gamelevel'].clock.get_time()
    update_shop(game_data["shop"], game_data["current_currency"], game_data["settings"],game_data["clicked"])
    update_tower(game_data["shop"],game_data["towers"], game_data, game_data['gamelevel'].monstertimeline, game_data["settings"],game_data["clicked"])
    if game_data['totalhp']>0 :
        Allenemydown=True
        for enemycreeps in game_data['gamelevel'].monstertimeline:
            damageFrame=0
            if enemycreeps['start_time']<game_data['gamelevel'].currenttime:
                enemycreeps['exist']=True   #enemy spawn , based on time line
            if enemycreeps['exist'] and enemycreeps['disappear']==False:
                if game_data['towers']==[]:
                    update_enemy(enemycreeps,game_data,game_data["towers"])
                else:
                    for tower in game_data["towers"]:        # if it is a combat tower,examine if the enemy is in range of the tower targeting dic
                        if tower.attack_mode!=0 and enemycreeps['CreepNo'] in tower.enemytarget.keys() and tower.nextattack<=0 : #if the enemycreeps is targeted and the tower is going to fire 
                            damageFrame+=tower.damage
                            tower.nextattack=1/tower.rate_of_fire*1000
                    update_enemy(enemycreeps,game_data,game_data["towers"],damageFrame)
            elif enemycreeps['disappear']==False:
                Allenemydown=False
        if Allenemydown==True:
            game_data["stay_open"]=2
    else :
        game_data["stay_open"]=2
                        


#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####

def render(game_data):
    ''' Rendering function - displays all objects to screen.
    Input: game_data
    Output: None
    '''
    render_map(game_data["map"], game_data["screen"], game_data["settings"])
    render_shop(game_data["shop"], game_data["screen"], game_data["settings"], game_data["current_currency"])
    for tower in game_data["towers"]:
        render_tower(tower, game_data["screen"], game_data["settings"])    
    for enemycreeps in game_data['gamelevel'].monstertimeline:
        if  enemycreeps['exist'] and enemycreeps['disappear']==False:   
            render_enemy(enemycreeps, game_data["screen"], game_data["settings"])
    scorefont=pygame.font.Font(None,30)
    colorinfo=(150,100,0)
    score1text=scorefont.render("Your HP:          {}  ".format(game_data['totalhp']),1,colorinfo)
    game_data["screen"].blit(score1text, (810, 600))   
    pygame.display.update()
def render2(gameData):
    ''' Replace this and the return statement with your code '''
    if gameData["stay_open"]==2:
        scorefont=pygame.font.Font(None,80)
        gameData["screen"].blit(gameData["Oversprite"],(0,0))
        overfont=pygame.font.Font(None,100)
        Ocolor=(250,10,0)
        #draw the name of socre 
        score1text=scorefont.render("Your HP:{}".format(gameData['totalhp']),1,Ocolor)                 
        gameData["screen"].blit(score1text, (350, 450))
        if gameData['totalhp']>0:
            overtext=overfont.render("You Win!",1,Ocolor)
        else:
            overtext=overfont.render("You Lose!",1,Ocolor)
        gameData["screen"].blit(overtext, (360,200))
        pygame.display.update()

#### ====================================================================================================================== ####
#############                                             MAIN                                                     #############
#### ====================================================================================================================== ####

def main():
    ''' Main function - initializes everything and then enters the primary game loop.
    Input: None
    Output: None
    '''
    # Initialize all required variables and objects
    game_data = initialize()
    pygame.mixer.music.load('764823_Dr-Madman-Father-of-the-Un.mp3')
    pygame.mixer.music.play(-1)
    # Begin Central Game Loop
    while game_data["stay_open"]!=0:
        if game_data["stay_open"]==1:
            process(game_data)
            update(game_data)
            render(game_data)
        elif game_data["stay_open"]==2:
            process(game_data)
            render2(game_data)
    # Exit pygame and Python
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
