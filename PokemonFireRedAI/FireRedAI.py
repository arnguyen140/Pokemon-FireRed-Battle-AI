import pyautogui as pyg
import pydirectinput as pyd
from win32gui import FindWindow, GetWindowRect, MoveWindow
from random import randint
import time

time.sleep(4)

# pyg.moveTo(1001,216)

# print(pyg.position())
# x,y = pyg.position()
# print(x,y)
# pixel = pyg.pixel(x,y)
# print(pixel)

#GetWindowRect(hwnd)
#height = 542 - 3 = 539
#width = 1370 - 634 = 736
#(x,y) = (634,3)
#(119,117,214)

#Do next --> pokemon_beat counter for leveling up and moves,
#white out at poke center, get parcel, 
#leave poke mart, save function, return parcel, enter lab

#Event variables
event_val = {
    'movewindow': 0,
    'startgame': 1,
    'options': 2,
    'getstarter': 3,
    'rival1': 4,
    'parcel': 5,
    'returnparcel': 6,
    'gym1': 7
    }
event = 'startgame'

#If want to take a break, set checkpoint = next objective
checkpoint = 'parcel'

#Move player variable
movement = 'normal'

#Battle variables
battle_type = 'off'
prev_move = ''
run_away = True
pokemon_beat = 0

#Leave building variable
leave_val = 0

#Variable to set position to get starter
go_down = 0

#Move game screen for color ID | To play game: File --> Open
if event == 'movewindow':
    pixel1 = pyg.pixel(645,3)
    pixel2 = pyg.pixel(645,534)
    pixel3 = pyg.pixel(1360,3)
    pixel4 = pyg.pixel(1360,534)
    
    if pixel1 == (119,117,214) and pixel2 == (119,117,214) and pixel3 == (119,117,214) and pixel4 == (119,117,214):
        event = 'startgame'
    
    hwnd = FindWindow(None,'VisualBoyAdvance')
    MoveWindow(hwnd,634,3,736,539,True)

#Save game every hour
#def save_game():

#Move player
def move(movement):
    
    which_move = randint(1,100)
    a = randint(1,4)
    b = randint(1,6)
    
    if movement == 'normal':
        if which_move <= 10:
            pyd.press('down',presses=b)
        elif which_move <= 25:
            pyd.press('left',presses=b)
        elif which_move <= 55:
            pyd.press('right',presses=a)
        elif which_move <= 100:
            pyd.press('up',presses=a)
        # elif which_move <= 100:
        #     pyd.press('down',presses=4)
        #     pyd.press('left',presses=4)
            
    if movement == 'supernormal':
        if which_move <= 2:
            pyd.press('down',presses=4)
        elif which_move <= 6:
            pyd.press('left',presses=4)
        elif which_move <= 46:
            pyd.press('right')
        elif which_move <= 100:
            pyd.press('up',presses=2)
        # elif which_move <= 100:
        #     pyd.press('down',presses=4)
        #     pyd.press('left',presses=4)
    
    if movement == 'reverse':
        if which_move <= 10:
            pyd.press('up',presses=b)
        elif which_move <= 25:
            pyd.press('right',presses=b)
        elif which_move <= 55:
            pyd.press('left',presses=a)
        elif which_move <= 100:
            pyd.press('down',presses=a)
        # elif which_move <= 100:
        #     pyd.press('right',presses=4)
        #     pyd.press('up',presses=4)
            
    if movement == 'superreverse':
        if which_move <= 2:
            pyd.press('up',presses=4)
        elif which_move <= 6:
            pyd.press('right',presses=4)
        elif which_move <= 46:
            pyd.press('left')
        elif which_move <= 100:
            pyd.press('down',presses=2)
        # elif which_move <= 100:
        #     pyd.press('up',presses=4)
        #     pyd.press('right',presses=4)
    
    if movement == 'select':
        if which_move <= 10:
            pyd.press('down')
        elif which_move <= 20:
            pyd.press('left')
        elif which_move <= 50:
            pyd.press('right')
        elif which_move <= 96:
            pyd.press('up')
        elif which_move <= 98:
            pyd.press('down',presses=3)
        elif which_move <= 100:
            pyd.press('left',presses=3)
            
    if movement == 'getparcel':
        if which_move <= 55:
            pyd.press('right')
        elif which_move <= 92:
            pyd.press('up')
        elif which_move <= 98:
            pyd.press('left',presses=3)
        elif which_move <= 100:
            pyd.press('down',presses=3)

#Battle
def battle(opponent):
    global event
    global movement
    global battle_type
    global prev_move
    global run_away
    global pokemon_beat
    
    battle_move = ''
    
    select_action = randint(1,10)
    which_move = randint(1,100)
    
    #Battle is over and player is in overworld
    # if player_hat == (0,0,0):
    #     print('checking to see if battle is done')
    #     time.sleep(3)
    if pyg.pixel(1001,268) == (248,104,72):
        print('battle is done')
        battle_type = 'off'
        battle_move = ''
        prev_move = ''
        
        global event
        if event == 'rival1':
            event = 'parcel'
        
        if opponent == 'wild' and run_away == False:
            run_away = True
            pokemon_beat += 1
        
        #White out and return home
        if pyg.pixel(1001,216) == (64,56,96) and pyg.pixel(996,133) == (160,144,48):
            movement = 'superreverse'
            
        #White out and return to Pokemon center
        
        
    #Action screen
    if battle_type != 'off' and pyg.pixel(1011,449) == (208,160,208) and pyg.pixel(1351,449) == (208,160,208):
        #Run away
        if opponent == 'wild' and select_action <= 3 and run_away == True:
            pyd.press('right')
            pyd.press('down')
            pyd.press('z')
        
        #Select a move
        else:
            run_away = False
            pyd.press('z')
            time.sleep(1)
    
    #Catch Pokemon
    #if opponent == 'wild' and event_val[event] > 6 and select_action > 3 and select_action <= 5:
    
    #Fight screen
    if battle_type != 'off' and pyg.pixel(651,449) == (208,160,208) and pyg.pixel(1112,449) == (208,160,208) and pyg.pixel(1351,449) == (208,160,208):
        run_away = False
        
        if which_move <= 40:
            battle_move = 'topleft'
            print(battle_move)
            if prev_move == 'topright':
                pyd.press('left')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'bottomright':
                pyd.press('up')
                time.sleep(0.5)
                pyd.press('left')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'bottomleft':
                pyd.press('up')
                time.sleep(0.5)
                pyd.press('z')
            else:
                pyd.press('z')
        
        elif which_move <= 60:
            battle_move = 'topright'
            print(battle_move)
            if prev_move == 'topright':
                pyd.press('z')
            elif prev_move == 'topleft':
                pyd.press('right')
                time.sleep(0.5)
                pyd.press('z') 
            elif prev_move == 'bottomright':
                pyd.press('up')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'bottomleft':
                pyd.press('up')
                time.sleep(0.5)
                pyd.press('right')
                time.sleep(0.5)
                pyd.press('z') 
            else:
                pyd.press('right')
                time.sleep(1)
                pyd.press('z')
            
        elif which_move <= 80:
            battle_move = 'bottomleft'
            print(battle_move)
            if prev_move == 'bottomleft':
                pyd.press('z')
            elif prev_move == 'topleft':
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'topright':
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('left')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'bottomright':
                pyd.press('left')
                time.sleep(0.5)
                pyd.press('z')
            else:
                pyd.press('down')
                time.sleep(1)
                pyd.press('z')
            
        elif which_move <= 100:
            battle_move = 'bottomright'
            print(battle_move)
            if prev_move == 'bottomright':
                pyd.press('z')
            elif prev_move == 'topleft':
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('right')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'topright':
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('z')
            elif prev_move == 'bottomleft':
                pyd.press('right')
                time.sleep(0.5)
                pyd.press('z')
            else:
                pyd.press('right')
                time.sleep(0.5)
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('z')
        
        prev_move = battle_move
        
    else:
        pyd.press('z')
        time.sleep(1)

#Choose Pokemon starter
def choose_starter(move_to,move_away):
    which_move = randint(1,4)
    if which_move == 1:
        pyd.press(move_to)
        time.sleep(1)
        pyd.press('z')
        time.sleep(1)
        pyd.press('z')
        time.sleep(1)
        pyd.press('x')
        pyd.press(move_away,presses=3)
    else:
        pyd.press(move_to)
        time.sleep(1)
        pyd.press('z')
        time.sleep(1)
        pyd.press('z')
        time.sleep(1)
        pyd.press('z')
        time.sleep(1)
        pyd.press('z')
        time.sleep(5.5)
        pyd.press('x')
        
        global event
        event = 'rival1'
        print(event + ' is next')
        
while False:
    #Pixel color identifiers
    player_hat = pyg.pixel(1001,268)
    
    #tborder = top border, bborder = bottom border
    tborder_outer1 = pyg.pixel(1001,405)
    tborder_outer2 = pyg.pixel(1001,401)
    
    bborder_outer1 = pyg.pixel(1001,520)
    bborder_outer2 = pyg.pixel(1001,522)
    
    #Start game
    if event == 'startgame':
        if player_hat == (248,104,72):
            print('start gameplay')
            event = checkpoint
        else:
            pyd.press('z')
    
    #Overworld text box
    if player_hat == (248,104,72) and tborder_outer1 == (160,208,224) and tborder_outer2 == (101,144,181) and bborder_outer1 == (160,208,224) and bborder_outer2 == (102,144,181):
        pyd.press('z')
    
    #Set options
    if event == 'options':
        menuborder_left = pyg.pixel(1157,204)
        menuborder_right = pyg.pixel(1351,204)
        
        if menuborder_left == (112,104,128) and menuborder_right == (112,104,128):
            pyd.press('down',presses=3)
            pyd.press('z')
            time.sleep(1)
            pyd.press('right')
            time.sleep(1)
            pyd.press('down',presses=4)
            time.sleep(1)
            pyd.press('right')
            time.sleep(1)
            pyd.press('down')
            time.sleep(1)
            pyd.press('left')
            time.sleep(1)
            pyd.press('z')
            time.sleep(1)
            pyd.press('up',presses=3)
            pyd.press('x')
            
            event = 'getstarter'
        else:
            pyd.press('enter')
    
    #Transition scene
    if player_hat != (248,104,72) and event_val[event] > 2 and battle_type == 'off': #(0,0,0)
        time.sleep(4)
        
        #Initiate trainer battle
        if pyg.pixel(1001,401) == (200,168,72) and pyg.pixel(1001,522) == (200,168,72) and pyg.pixel(1227,453) == (40,80,104) and pyg.pixel(910,258) == (248,112,88) and pyg.pixel(880,156) == (248,176,64):
            battle_type = 'trainer'
            time.sleep(0.5)
            pyd.press('z')
            print('trainer battle')
            time.sleep(3)
            
        #Initiate wild battle
        elif pyg.pixel(1001,401) == (200,168,72) and pyg.pixel(1001,522) == (200,168,72) and pyg.pixel(1227,453) == (40,80,104) and pyg.pixel(910,258) == (248,112,88):
            battle_type = 'wild'
            time.sleep(0.5)
            pyd.press('z')
            print('wild battle')
            time.sleep(3)
            
        #Check if player is in overworld
        elif pyg.pixel(1001,268) == (248,104,72):
            floor1 = pyg.pixel(1037,289)
            floor2 = pyg.pixel(963,289)
            floor3 = pyg.pixel(999,241)
            
            outside_u = pyg.pixel(1007,72)
            outside_d = pyg.pixel(1007,481)
            outside_r = pyg.pixel(1318,268)
            outside_l = pyg.pixel(656,268)
            
            #Leave player's house or any similar building
            if floor1 == (160,144,48) or floor2 == (160,144,48) or floor3 == (192,176,72):
                leave_val += 1
                print('leave_val is ' + str(leave_val))
                
                if leave_val % 2:
                    movement = 'superreverse'
                    print('movement is super reverse')
                else:
                    movement = 'normal'
                    print('movement is normal')
            
            # #Inside the Pokemon lab
            # elif event == 'getstarter' and pyg.pixel(1001,253) == (248,248,248) and pyg.pixel(1001,222) == (200,168,96):
            #     movement = 'select'
            #     print('movement is select')
            
            #Leave Pokemon lab
            elif pyg.pixel(872,100) == (184,96,72) and pyg.pixel(1145,120) == (192,184,208):
                movement = 'superreverse'
                print('movement is super reverse')
            
            #Outside a building/transition scene
            elif outside_u != (0,0,0) and outside_d != (0,0,0) and outside_r != (0,0,0) and outside_l != (0,0,0):
                movement = 'normal'
                leave_val = 0
                print('movement is normal')
    
    #Get Pokemon starter
    if event == 'getstarter':
        #Once inside the Pokemon lab, go down to set position for getting starter
        if go_down < 23:
            if movement != '' and pyg.pixel(1001,249) == (224,104,72) and pyg.pixel(1001,217) == (200,168,96) and pyg.pixel(881,482) == (224,136,96):
                movement = ''
                print('movement is off')
                go_down += 1
            
            if go_down > 0:
                pyd.press('down')
                go_down += 1
            
            if go_down == 23:
                movement = 'select'
                print('movement is select')
                
        #Directions relative to player: u = up, d = down, l = left, r = right
        player_u1 = pyg.pixel(1000,245)
        player_ur1 = pyg.pixel(1015,241)

        player_d1 = pyg.pixel(1000,341)
        player_dr1 = pyg.pixel(1014,337)

        player_r1 = pyg.pixel(1048,295)
        player_ru1 = pyg.pixel(1062,289)

        player_ld1 = pyg.pixel(952,293)
        player_l1 = pyg.pixel(965,289)
        
        #Choose Pokemon starter
        if player_u1 == (224,104,72) and player_ur1 == (136,192,136):
            choose_starter('up','down')
        if player_d1 == (224,104,72) and player_dr1 == (136,192,136):
            choose_starter('down','up')
        if player_r1 == (224,104,72) and player_ru1 == (136,192,136):
            choose_starter('right','down')
        if player_ld1 == (224,104,72) and player_l1 == (136,192,136):
            choose_starter('left','down')
    
    #Rival battle 1
    if event == 'rival1':
        if player_hat == (248,104,72):
            movement = 'superreverse'
    
    #Enter Viridian City to get parcel
    #if event == 'parcel':
        #if pyg.pixel() == and pyg.pixel() == :
            #movement = 'getparcel'
        #Enter Poke mart
        #if pyg.pixel() == :
            #pyd.press('up',presses=2)
            #time.sleep(3)
            #pyd.press('up',presses=5)
            #pyd.press('left')
            #pyd.press('z')
            #movement = 'superreverse'
            #event = 'returnparcel'
    
    #Return parcel to Professor Oak
    #if event == 'returnparcel':
        #movement = 'reverse'
    
    #Battle
    if battle_type != 'off':
        battle(battle_type)
    
    #Move in overworld
    if player_hat == (248,104,72) and event_val[event] > 2:
        move(movement)
    
    
    
    
    
    
    
    
