import re
import cv2
import mss
import time
import math
import random
import ctypes
import subprocess
import numpy as np
import pandas as pd
import difflib as dfl
import pypokedex as pyp
import pytesseract as pyt
import pydirectinput as pyd
from PIL import Image, ImageGrab, ImageOps
from win32gui import FindWindow, GetWindowRect, MoveWindow

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# time.sleep(3)

# Sizing for VisualBoyAdvance
hwnd = FindWindow(None, 'VisualBoyAdvance')
MoveWindow(hwnd, 989, 19, 920, 674, True)

# Image to text idenifier
pyt.pytesseract.tesseract_cmd = type path here

# List of all gen 1 Pokemon names
Gen1_Pokemon = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard', 'Squirtle', 'Wartortle', 
           'Blastoise', 'Caterpie', 'Metapod', 'Butterfree', 'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 
           'Pidgeot', 'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok', 'Pikachu', 'Raichu', 'Sandshrew', 
           'Sandslash', 'Nidoran-F', 'Nidorina', 'Nidoqueen', 'Nidoran-M', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable', 
           'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat', 'Oddish', 'Gloom', 'Vileplume', 'Paras', 
           'Parasect', 'Venonat', 'Venomoth', 'Diglett', 'Dugtrio', 'Meowth', 'Persian', 'Psyduck', 'Golduck', 'Mankey', 
           'Primeape', 'Growlithe', 'Arcanine', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam', 'Machop', 
           'Machoke', 'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel', 'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 
           'Golem', 'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetch\'d', 'Doduo', 'Dodrio', 'Seel', 
           'Dewgong', 'Grimer', 'Muk', 'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix', 'Drowzee', 'Hypno', 'Krabby', 
           'Kingler', 'Voltorb', 'Electrode', 'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan', 'Lickitung', 
           'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey', 'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking', 
           'Staryu', 'Starmie', 'Mr. Mime', 'Scyther', 'Jynx', 'Electabuzz', 'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 
           'Lapras', 'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon', 'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 
           'Aerodactyl', 'Snorlax', 'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite', 'Mewtwo', 'Mew']

# Get list of all gen 1 to gen 3 pokemon moves
df = pd.read_csv('Pokemon Moves.csv')
Gens1to3_Moves = df['Name'].tolist()

df2 = pd.read_csv('Pokemon Types.csv')

df3 = pd.read_csv('Type Effectiveness.csv')

status_moves = {
    'Swords Dance': (2, 'atk', 'user'), 
    'Tail Whip': (-1, 'def', 'target'), 
    'Leer': (-1, 'def', 'target'),
    'Growl': (-1, 'atk', 'target'),
    'Growth': (1, 'spa', 'user'), 
    'String Shot': (-1, 'spe', 'target'), 
    'Meditate': (1, 'atk', 'user'), 
    'Agility': (2, 'spe', 'user'), 
    'Screech': (-2, 'def', 'target'), 
    'Harden': (1, 'def', 'user'), 
    'Withdraw': (1, 'def', 'user'), 
    'Defense Curl': (1, 'def', 'user'), 
    'Barrier': (2, 'def', 'user'), 
    'Skull Bash': (1, 'def', 'user'), 
    'Amnesia': (2, 'spd', 'user'), 
    'Acid Armor': (2, 'def', 'user'), 
    'Sharpen': (1, 'atk', 'user'), 
    'Curse': (1, 'atk', 1, 'def', -1, 'spe', 'user'), 
    'Cotton Spore': (-2, 'spe', 'target'), 
    'Scary Face': (-2, 'spe', 'target'), 
    'Belly Drum': (6, 'atk', 'user'), 
    'Icy Wind': (-1, 'spe', 'target'), 
    'Charm': (-2, 'atk', 'target'), 
    'Swagger': (2, 'atk', 'target'), 
    'Stockpile': (1, 'def', 1, 'spd', 'user'), 
    'Flatter': (1, 'spa', 'target'), 
    'Memento': (-2, 'atk', -2, 'spa', 'target'), 
    'Superpower': (-1, 'atk', -1, 'def', 'user'), 
    'Tail Glow': (2, 'spa', 'user'), 
    'FeatherDance': (-2, 'atk', 'target'), 
    'Fake Tears': (-2, 'spd', 'target'), 
    'Overheat': (-2, 'spa', 'user'), 
    'Rock Tomb': (-1, 'spe', 'target'), 
    'Metal Sound': (-2, 'spd', 'target'), 
    'Tickle': (-1, 'atk', -1, 'def', 'target'), 
    'Cosmic Power': (1, 'def', 1, 'spd', 'user'), 
    'Iron Defense': (2, 'def', 'user'), 
    'Howl': (1, 'atk', 'user'), 
    'Bulk Up': (1, 'atk', 1, 'def', 'user'), 
    'Mud Shot': (-1, 'spe', 'target'), 
    'Calm Mind': (1, 'spa', 1, 'spd', 'user'), 
    'Dragon Dance': (1, 'atk', 1, 'spe', 'user'), 
    'Psycho Boost': (-2, 'spa', 'user')
}

physical_types = ['Normal', 'Fighting', 'Poison', 'Ground', 'Flying', 'Bug', 'Rock', 'Ghost', 'Steel']

# move_name = ''

# get_move_power = df.query('Name==\'{}\''.format(move_name))['Power']

# move_power = int(float(get_move_power.to_string(index=False)))

# get_move_type = df.query(f'Name==\'{move_name}\'')['Type']

# move_type = get_move_type.to_string(index=False)

def select_move(which_move):
    global prev_move

    if which_move == 1:
        battle_move = 1
        if prev_move == 2:
            pyd.press('left')
        elif prev_move == 3:
            pyd.press('up')
        elif prev_move == 4:
            pyd.press('up')
            pyd.press('left')
        
    elif which_move == 2:
        battle_move = 2
        if prev_move in (0, 1):
            pyd.press('right')
        elif prev_move == 3:
            pyd.press('up')
            pyd.press('right')
        elif prev_move == 4:
            pyd.press('up')
            
    elif which_move == 3:
        battle_move = 3
        if prev_move in (0, 1):
            pyd.press('down')
        elif prev_move == 2:
            pyd.press('down')
            pyd.press('left')
        elif prev_move == 4:
            pyd.press('left')

    elif which_move == 4:
        battle_move = 4
        if prev_move in (0, 1):
            pyd.press('down')
            pyd.press('right')
        elif prev_move == 2:
            pyd.press('down')
        elif prev_move == 3:
            pyd.press('right')
    
    prev_move = battle_move

# Set which_Pokemon to 'plyr' to get name of Player's Pokemon. Any other value gets opposing Pokemon's name. 
def get_pokemon_name(which_Pokemon):
        # Player Pokemon
        with mss.mss() as sct:
            if which_Pokemon == 'plyr':
                # Get name in bottom left dark blue background bbox=(1029, 585, 1275, 665)
                # Get name above HP bbox=(1518, 368, 1730, 418)
                mon_name_img = sct.grab((1518, 368, 1730, 418))
            
            elif which_Pokemon == 'slot2':
                mon_name_img = sct.grab((1432, 132, 1633, 173))

            elif which_Pokemon == 'slot3':
                mon_name_img = sct.grab((1432, 222, 1633, 263))

            elif which_Pokemon == 'slot4':
                mon_name_img = sct.grab((1432, 312, 1633, 353))

            elif which_Pokemon == 'slot5':
                mon_name_img = sct.grab((1432, 402, 1633, 443))

            elif which_Pokemon == 'slot6':
                mon_name_img = sct.grab((1432, 492, 1633, 533))

            # Opposing Pokemon
            else:
                mon_name_img = sct.grab((1058, 150, 1270, 198))

        mon_name_img = Image.frombytes('RGB', mon_name_img.size, mon_name_img.bgra, 'raw', 'BGRX')

        thresh = 171
        fn = lambda x : 255 if x > thresh else 0
        mon_name_img = mon_name_img.convert('L').point(fn, mode='1')

        mon_name = pyt.image_to_string(mon_name_img, config='--psm 7')
        mon_name = mon_name.capitalize()

        if (mon_name.find('R. ') == 0 or mon_name.find('r. ') in (1, 2)) and ('m' in mon_name or 'n' in mon_name) and 'i' in mon_name and 'e' in mon_name:
            mon_name_readjusted = 'Mr. Mime'
        
        else:
            mon_name_readjusted = re.sub('[^a-zA-Z]', '', mon_name)

        return dfl.get_close_matches(mon_name_readjusted, Gen1_Pokemon, cutoff=0.1)[0]

# # print(get_pokemon_name('plyr'))

def get_pokemon_level(which_Pokemon):
    with mss.mss() as sct:
        if which_Pokemon == 'plyr':
            mon_lvl_img = sct.grab((1735, 368, 1838, 415))

        else:
            mon_lvl_img = sct.grab((1275, 150, 1378, 198))

    mon_lvl_img = Image.frombytes('RGB', mon_lvl_img.size, mon_lvl_img.bgra, 'raw', 'BGRX')
    
    thresh = 171
    fn = lambda x : 255 if x > thresh else 0
    mon_lvl_img = mon_lvl_img.convert('L').point(fn, mode='1')

    mon_lvl = pyt.image_to_string(mon_lvl_img, config='--psm 10')
    
    mon_lvl = mon_lvl[2:]
    mon_lvl = mon_lvl.lower()
    
    mon_lvl = mon_lvl.replace('la', '14')
    mon_lvl = mon_lvl.replace('?', '7')
    mon_lvl = mon_lvl.replace('s', '5')
    mon_lvl = mon_lvl.replace('d', '4')
    mon_lvl = mon_lvl.replace('q', '4')
    mon_lvl = mon_lvl.replace('l', '1')
    mon_lvl = mon_lvl.replace('i', '1')
    mon_lvl = mon_lvl.replace('o', '0')

    mon_lvl = re.sub('[^\d]', '', mon_lvl)

    if len(mon_lvl) > 2 and '00' not in mon_lvl:
        mon_lvl = mon_lvl[1:]

    if mon_lvl == '':
        return 'empty'
    else:
        return mon_lvl

# # print(get_pokemon_level('plyr'))

def get_color(x, y):
    # img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    with mss.mss() as sct:
        img = sct.grab((x, y, x+1, y+1))
    img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
    return img.getpixel((0, 0))

def get_pokemon_HP(which_Pokemon):
    if which_Pokemon == 'plyr':
        x, y = 1829, 433
        limit = 1654
    
    else:
        x, y = 1371, 212
        limit = 1196

    while x >= limit:
        color = get_color(x, y)
        if (color not in ((97, 118, 104), (87, 108, 87), (82, 105, 89), (80, 104, 88), (80, 103, 88), (81, 104, 88), (81, 105, 89), (79, 71, 94), (73, 65, 89))) or (x == limit + 1):
            # returns a percent that is an integer without the percent sign e.g. return value of 3 = 3%
            return math.ceil(((x - limit)/175) * 100)

        x -= 1

# # print(get_pokemon_HP('plyr'))

# Gets HP of a single party member
def get_party_HP(x, y, limit):
    while x >= limit:
        color = get_color(x, y)
        if (color not in ((112, 112, 112), (126, 126, 126))) or (x == limit + 1):
            # returns a percent that is an integer without the percent sign e.g. return value of 3 = 3%
            return math.ceil(((x - limit)/175) * 100)
        x -= 2

def get_party_status():
    party = []
    x = 1867
    limit = 1692
    if (get_color(1867, 135) == (56, 144, 216)):
        # slot number refers to position in party with slot 1 being the lead Pokemon
        y = 156
        slot2 = ('slot2', get_pokemon_name('slot2'), get_party_HP(x, y, limit))
        party.append(slot2)
        
    if (get_color(1867, 225) == (56, 144, 216)):
        y = 246
        slot3 = ('slot3', get_pokemon_name('slot3'), get_party_HP(x, y, limit))
        party.append(slot3)

    if (get_color(1867, 315) == (56, 144, 216)):
        y = 336
        slot4 = ('slot4', get_pokemon_name('slot4'), get_party_HP(x, y, limit))
        party.append(slot4)
            
    if (get_color(1867, 405) == (56, 144, 216)):
        y = 426
        slot5 = ('slot5', get_pokemon_name('slot5'), get_party_HP(x, y, limit))
        party.append(slot5)

    if (get_color(1867, 495) == (56, 144, 216)):
        y = 516
        slot6 = ('slot6', get_pokemon_name('slot6'), get_party_HP(x, y, limit))
        party.append(slot6)
    
    return party

# for obj in get_party_status():
#     # print(obj)

# Set which_move to an integer --> 1 = top left move, 2 = top right move, 3 = bottom left move, int >= 4 = bottom right move
def get_pokemon_move(which_move):
    with mss.mss() as sct:
        if which_move == 1:
            move_img = sct.grab((1050, 540, 1310, 590))
            
        elif which_move == 2:
            move_img = sct.grab((1315, 540, 1575, 590))
            
        elif which_move == 3:
            move_img = sct.grab((1050, 600, 1310, 650))
            
        else:
            move_img = sct.grab((1315, 600, 1575, 650))
    move_img = np.array(move_img)
    move_name = pyt.image_to_string(move_img, config='--psm 7')
    move_name = move_name.capitalize()
    
    move_name_readjusted = re.sub('[^a-zA-Z-]', '', move_name)

    if move_name_readjusted == '' or move_name_readjusted == '-':
        return 'empty'

    return which_move, dfl.get_close_matches(move_name_readjusted, Gens1to3_Moves, cutoff=0.1)[0]

# # print(get_pokemon_move(2))

def get_moveset(mon_name, lvl):
    p = pyp.get(name=mon_name)
    moves = []
    
    for move in p.moves['firered-leafgreen']:
        if move[1] == 'level-up' and move[2] <= lvl:
            moves.append(move)

    moves.sort(key=lambda x: x[2])
    moves = moves[-4:]
    move_names = []
    
    for move in moves:
        move_names.append(move[0])
    
    return move_names

def get_move_type(move_name):
    get_move_type = df.query(f'Name==\'{move_name}\'')['Type']
    return get_move_type.to_string(index=False)

def get_mon_type(mon_name):
    mon_type = df2.query(f'Name==\'{mon_name}\'')['Type']
    return mon_type.to_string(index=False).split(' ')

def get_type_relation(typing1, typing2):
    type_relation = df3.query(f'Type==\'{typing1}\'')[typing2]
    return float(type_relation.to_string(index=False))

def get_move_accuracy(move_name):
    move_acc = df.query(f'Name==\'{move_name}\'')['Accuracy']
    move_acc = move_acc.to_string(index=False)
    if move_acc == 'NaN':
        move_acc = 100
    else:
        move_acc = int(move_acc[:-1])    
    return move_acc

def get_move_score(move_name, move1, move2, move3, move4, mon, learned):
    move_power = df.query(f'Name==\'{move_name}\'')['Power']
    move_power = move_power.to_string(index=False)
    if move_power == 'NaN':
        move_power = 0
    else:
        move_power = int(move_power)
    move_acc = df.query(f'Name==\'{move_name}\'')['Accuracy']
    move_acc = move_acc.to_string(index=False)
    if move_acc != 'NaN':
        move_acc = int(move_acc[:-1])

    move_type = get_move_type(move_name)
    p = pyp.get(name=mon)
    bst = 0
    for i in p.base_stats:
        bst += i

    score = 0
    if move_name in ('Selfdestruct', 'Explosion', 'Memento'):
        score = -1
    elif move_power == 0:
        if move_acc == 'NaN':
            score += 1.3
        else:
            score += (move_acc/100) * (((move_acc/100)/0.7) ** 1.25)
        if move_name in status_moves:
            if len(status_moves[move_name]) == 3:
                if (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'atk' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'def' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[1] >= p.base_stats[3]:
                        score += 1
                    for i in get_mon_type(mon):
                        if i in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1, move2, move3, move4):
                        if learned == False or i != move4:
                            move_power_again = df.query(f'Name==\'{i}\'')['Power']
                            move_power_again = move_power_again.to_string(index=False)
                            if move_power_again == 'NaN':
                                move_power_again = 0
                            else:
                                move_power_again = int(move_power_again)
                            if move_power_again > 0 and get_move_type(i) in physical_types:
                                boost += 1.5
                    if boost > 0:
                        if status_moves[move_name][0] > 0:
                            score += 1
                        if status_moves[move_name][0] > 1:
                            score += 1.5
                        if status_moves[move_name][0] < 0:
                            score += 0.5
                        if status_moves[move_name][0] < -1:
                            score += 1
                    score += min(boost, 4.5)
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'spa' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'spd' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[3] >= p.base_stats[1]:
                        score += 1
                    for i in get_mon_type(mon):
                        if i not in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1, move2, move3, move4):
                        if learned == False or i != move4:
                            move_power_again = df.query(f'Name==\'{i}\'')['Power']
                            move_power_again = move_power_again.to_string(index=False)
                            if move_power_again == 'NaN':
                                move_power_again = 0
                            else:
                                move_power_again = int(move_power_again)
                            if move_power_again > 0 and get_move_type(i) not in physical_types:
                                boost += 1.5
                    if boost > 0:
                        if status_moves[move_name][0] > 0:
                            score += 1
                        if status_moves[move_name][0] > 1:
                            score += 1.5
                        if status_moves[move_name][0] < 0:
                            score += 0.5
                        if status_moves[move_name][0] < -1:
                            score += 1
                    score += min(boost, 4.5)
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'def' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'atk' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[2] <= p.base_stats[4]:
                        score += 2
                    if status_moves[move_name][0] > 0:
                        score += 1.5
                    if status_moves[move_name][0] > 1:
                        score += 2.5
                    if status_moves[move_name][0] < 0:
                        score += 1.5
                    if status_moves[move_name][0] < -1:
                        score += 2
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'spd' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'spa' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[4] <= p.base_stats[2]:
                        score += 2
                    if status_moves[move_name][0] > 0:
                        score += 1.5
                    if status_moves[move_name][0] > 1:
                        score += 2.5
                    if status_moves[move_name][0] < 0:
                        score += 1.5
                    if status_moves[move_name][0] < -1:
                        score += 2
                elif status_moves[move_name][1] == 'spe':
                    if p.base_stats[5] <= 85:
                        score += 2
                    if status_moves[move_name][0] > 0:
                        score += 1.5
                    if status_moves[move_name][0] > 1:
                        score += 2.5
                    if status_moves[move_name][0] < 0:
                        score += 1.5
                    if status_moves[move_name][0] < -1:
                        score += 2
            
            elif len(status_moves[move_name]) == 5:
                score += 1
                if (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'atk' and status_moves[move_name][4] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'def' and status_moves[move_name][4] == 'target'):
                    if p.base_stats[1] >= p.base_stats[3]:
                        score += 1
                    if status_moves[move_name][2] > 0 and status_moves[move_name][3] == 'spe' and status_moves[move_name][4] == 'user':
                        score += 1
                    for i in get_mon_type(mon):
                        if i in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1, move2, move3, move4):
                        if learned == False or i != move4:
                            move_power_again = df.query(f'Name==\'{i}\'')['Power']
                            move_power_again = move_power_again.to_string(index=False)
                            if move_power_again == 'NaN':
                                move_power_again = 0
                            else:
                                move_power_again = int(move_power_again)
                            if move_power_again > 0 and get_move_type(i) in physical_types:
                                boost += 1.5
                    if boost > 0:
                        if status_moves[move_name][0] > 0:
                            score += 1
                        if status_moves[move_name][0] > 1:
                            score += 1.5
                        if status_moves[move_name][0] < 0:
                            score += 0.5
                        if status_moves[move_name][0] < -1:
                            score += 1
                    score += min(boost, 4.5)
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'spa' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'spd' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[3] >= p.base_stats[1]:
                        score += 1
                    if status_moves[move_name][2] > 0 and status_moves[move_name][3] == 'spe' and status_moves[move_name][4] == 'user':
                        score += 1
                    for i in get_mon_type(mon):
                        if i not in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1, move2, move3, move4):
                        if learned == False or i != move4:
                            move_power_again = df.query(f'Name==\'{i}\'')['Power']
                            move_power_again = move_power_again.to_string(index=False)
                            if move_power_again == 'NaN':
                                move_power_again = 0
                            else:
                                move_power_again = int(move_power_again)
                            if move_power_again > 0 and get_move_type(i) not in physical_types:
                                boost += 1.5
                    if boost > 0:
                        if status_moves[move_name][0] > 0:
                            score += 1
                        if status_moves[move_name][0] > 1:
                            score += 1.5
                        if status_moves[move_name][0] < 0:
                            score += 0.5
                        if status_moves[move_name][0] < -1:
                            score += 1
                    score += min(boost, 4.5)
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'def' and status_moves[move_name][4] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'atk' and status_moves[move_name][4] == 'target'):
                    if p.base_stats[2] <= p.base_stats[4]:
                        score += 2
                    if status_moves[move_name][0] > 0:
                        score += 1.5
                    if status_moves[move_name][0] > 1:
                        score += 2.5
                    if status_moves[move_name][0] < 0:
                        score += 1.5
                    if status_moves[move_name][0] < -1:
                        score += 2
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'spd' and status_moves[move_name][4] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'spa' and status_moves[move_name][4] == 'target'):
                    if p.base_stats[4] <= p.base_stats[2]:
                        score += 2
                    if status_moves[move_name][0] > 0:
                        score += 1.5
                    if status_moves[move_name][0] > 1:
                        score += 2.5
                    if status_moves[move_name][0] < 0:
                        score += 1.5
                    if status_moves[move_name][0] < -1:
                        score += 2
            else:
                score += 2
                if move_name == 'Curse' and 'Ghost' in get_mon_type(mon):
                    score += -3
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'atk' and status_moves[move_name][6] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'def' and status_moves[move_name][6] == 'target'):
                    if p.base_stats[1] >= p.base_stats[3]:
                        score += 1
                    if status_moves[move_name][4] > 0 and status_moves[move_name][5] == 'spe' and status_moves[move_name][6] == 'user':
                        score += 1
                    elif status_moves[move_name][4] < 0 and status_moves[move_name][5] == 'spe' and status_moves[move_name][6] == 'user':
                        score += -2
                    for i in get_mon_type(mon):
                        if i in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1, move2, move3, move4):
                        if learned == False or i != move4:
                            move_power_again = df.query(f'Name==\'{i}\'')['Power']
                            move_power_again = move_power_again.to_string(index=False)
                            if move_power_again == 'NaN':
                                move_power_again = 0
                            else:
                                move_power_again = int(move_power_again)
                            if move_power_again > 0 and get_move_type(i) in physical_types:
                                boost += 1.5
                    if boost > 0:
                        if status_moves[move_name][0] > 0:
                            score += 1
                        if status_moves[move_name][0] > 1:
                            score += 1.5
                        if status_moves[move_name][0] < 0:
                            score += 0.5
                        if status_moves[move_name][0] < -1:
                            score += 1
                    score += min(boost, 4.5)

        elif move_name == 'Will-O-Wisp':
            score += 1.5 * 1.8
            if bst <= 350 and ((p.base_stats[0] + p.base_stats[2])/ 2) <= 50:
                score += 1.25
            elif bst <= 435 and ((p.base_stats[0] + p.base_stats[2])/ 2) <= 70:
                score += 1.25
            elif bst <= 530 and ((p.base_stats[0] + p.base_stats[2])/ 2) <= 80:
                score += 1.25
            elif bst > 530 and ((p.base_stats[0] + p.base_stats[2])/ 2) <= 90:
                score += 1.25

        elif move_name == 'PoisonPowder':
            score += 1 * 1.8
            if bst <= 350 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 50:
                score += 1.25
            elif bst <= 435 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 70:
                score += 1.25
            elif bst <= 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 80:
                score += 1.25
            elif bst > 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 90:
                score += 1.25

        elif move_name == 'Toxic':
            score += 3 * 1.8
            if bst <= 350 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 50:
                score += 1.25
            elif bst <= 435 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 70:
                score += 1.25
            elif bst <= 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 80:
                score += 1.25
            elif bst > 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 90:
                score += 1.25

        elif move_name in ('GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn'):
            score += 2 * 1.8
            if bst <= 350 and (p.base_stats[5] >= 40 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 50):
                score += 1.25
            elif bst <= 435 and (p.base_stats[5] >= 70 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 70):
                score += 1.25
            elif bst <= 530 and (p.base_stats[5] >= 75 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 80):
                score += 1.25
            elif bst > 530 and (p.base_stats[5] >= 80 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 90):
                score += 1.25

        elif move_name in ('Glare', 'Stun Spore', 'Thunder Wave'):
            score += 2.5 * 1.8
            if bst <= 350 and p.base_stats[5] <= 40:
                score += 1.25
            elif bst <= 435 and p.base_stats[5] <= 70:
                score += 1.25
            elif bst <= 530 and p.base_stats[5] <= 80:
                score += 1.25
            elif bst > 530 and p.base_stats[5] <= 90:
                score += 1.25
        
        elif move_name in ('Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance'):
            score += 0.5 * 1.8
        
        elif move_name == 'Leech Seed':
            score += 2.25 * 1.8
            if bst <= 350 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 50:
                score += 1.25
            elif bst <= 435 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 70:
                score += 1.25
            elif bst <= 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 80:
                score += 1.25
            elif bst > 530 and ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 90:
                score += 1.25

        elif move_name in ('Recover', 'Morning Sun', 'Synthesis', 'Moonlight'):
            score += 4.5 * 1.8
                    
    elif move_name in ('Cut', 'Fly', 'Surf', 'Strength', 'Flash', 'Rock Smash', 'Waterfall') and learned == True:
        score = 1000

    else:
        score += (move_power/100) * (((move_power/100)/0.5) ** 0.3)
        score += (move_acc/100) * (((move_acc/100)/0.65) ** 1.25)
        for i in get_mon_type(mon):
            if move_type == i:
                score += 1
        if move_type in physical_types and p.base_stats[1] >= p.base_stats[3]:
            score += 1
        elif move_type not in physical_types and p.base_stats[3] >= p.base_stats[1]:
            score += 1
        compare_moves = []
        for i in (move1, move2, move3, move4):
            move_power_again = df.query(f'Name==\'{i}\'')['Power']
            move_power_again = move_power_again.to_string(index=False)
            if move_power_again == 'NaN':
                move_power_again = 0
            else:
                move_power_again = int(move_power_again)
            if move_power_again > 0:
                compare_moves.append(i)
        move_types = []
        for i in compare_moves:
            move_types.append(get_move_type(i))
        if get_move_type(move_name) not in move_types:
            score += 1.5
        my_mon_type = get_mon_type(mon)
        for i in df3['Type'].tolist():
            if get_type_relation(i, move_type) == 0.5:
                score += 0.1
            elif get_type_relation(i, move_type) == 1:
                score += 0.2
            elif get_type_relation(i, move_type) == 2 and ((len(my_mon_type) == 1 and get_type_relation(my_mon_type[0], i) >= 2)
            or (len(my_mon_type) == 2 and get_type_relation(my_mon_type[0], i) * get_type_relation(my_mon_type[1], i) >= 2)):
                score += 0.5
            elif get_type_relation(i, move_type) == 2 and ((len(my_mon_type) == 1 and get_type_relation(i, my_mon_type[0]) <= 1)
            or (len(my_mon_type) == 2 and get_type_relation(i, my_mon_type[0]) <= 1 and get_type_relation(i, my_mon_type[1]) <= 1)):
                score += 0.4
            elif get_type_relation(i, move_type) == 2:
                score += 0.35
        if move_name in ('Bounce', 'Dig', 'Dive', 'Fly', 'Focus Punch', 'Razor Wind', 'Skull Bash', 'Sky Attack', 'SolarBeam'):
            score = score * 0.8
        elif move_name in ('Hyper Beam', 'Frenzy Plant', 'Blast Burn', 'Hydro Cannon'):
            score = score * 0.85
        elif move_name in ('Outrage', 'Petal Dance'):
            score = score * 0.9
        elif move_power < 60:
            score = score ** 0.85
    return score

# # print(get_move_score('Slash', 'Water Spout', 'Meteor Mash', 'Earthquake', 'Tackle', 'Snorlax', False))

def learn_move():
    with mss.mss() as sct:
        move1_img = sct.grab((1581, 163, 1890, 208))
        move1_img = np.array(move1_img)
        move1_name = pyt.image_to_string(move1_img, config='--psm 7')
        move1_name = move1_name.capitalize()
        move1_name = re.sub('[^a-zA-Z-]', '', move1_name)
        move1_name = dfl.get_close_matches(move1_name, Gens1to3_Moves, cutoff=0.1)[0]

        move1_power = df.query(f'Name==\'{move1_name}\'')['Power']
        move1_power = move1_power.to_string(index=False)
        if move1_power == 'NaN':
            move1_power = 0
        else:
            move1_power = int(move1_power)

        move2_img = sct.grab((1581, 268, 1890, 313))
        move2_img = np.array(move2_img)
        move2_name = pyt.image_to_string(move2_img, config='--psm 7')
        move2_name = move2_name.capitalize()
        move2_name = re.sub('[^a-zA-Z-]', '', move2_name)
        move2_name = dfl.get_close_matches(move2_name, Gens1to3_Moves, cutoff=0.1)[0]

        move2_power = df.query(f'Name==\'{move2_name}\'')['Power']
        move2_power = move2_power.to_string(index=False)
        if move2_power == 'NaN':
            move2_power = 0
        else:
            move2_power = int(move2_power)
        
        move3_img = sct.grab((1581, 373, 1890, 418))
        move3_img = np.array(move3_img)
        move3_name = pyt.image_to_string(move3_img, config='--psm 7')
        move3_name = move3_name.capitalize()
        move3_name = re.sub('[^a-zA-Z-]', '', move3_name)
        move3_name = dfl.get_close_matches(move3_name, Gens1to3_Moves, cutoff=0.1)[0]

        move3_power = df.query(f'Name==\'{move3_name}\'')['Power']
        move3_power = move3_power.to_string(index=False)
        if move3_power == 'NaN':
            move3_power = 0
        else:
            move3_power = int(move3_power)

        move4_img = sct.grab((1581, 478, 1890, 523))
        move4_img = np.array(move4_img)
        move4_name = pyt.image_to_string(move4_img, config='--psm 7')
        move4_name = move4_name.capitalize()
        move4_name = re.sub('[^a-zA-Z-]', '', move4_name)
        move4_name = dfl.get_close_matches(move4_name, Gens1to3_Moves, cutoff=0.1)[0]

        move4_power = df.query(f'Name==\'{move4_name}\'')['Power']
        move4_power = move4_power.to_string(index=False)
        if move4_power == 'NaN':
            move4_power = 0
        else:
            move4_power = int(move4_power)

        move5_img = sct.grab((1581, 583, 1890, 628))
        hsv = cv2.cvtColor(np.array(move5_img), cv2.COLOR_BGR2HSV)
        lower_val = np.array([0, 0, 0])
        upper_val = np.array([145, 145, 145])
        mask = cv2.inRange(hsv, lower_val, upper_val)
        pil_image = Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
        move5_name = pyt.image_to_string(pil_image, config='--psm 7')
        move5_name = move5_name.capitalize()
        move5_name = re.sub('[^a-zA-Z-]', '', move5_name)
        move5_name = dfl.get_close_matches(move5_name, Gens1to3_Moves, cutoff=0.1)[0]

        move5_power = df.query(f'Name==\'{move5_name}\'')['Power']
        move5_power = move5_power.to_string(index=False)
        if move5_power == 'NaN':
            move5_power = 0
        else:
            move5_power = int(move5_power)
        # get mon name
        # tiebreaker is pp
        mon_name_img = sct.grab((1122, 150, 1389, 208))
        mon_name_img = Image.frombytes('RGB', mon_name_img.size, mon_name_img.bgra, 'raw', 'BGRX')
        inv_img = ImageOps.invert(mon_name_img)
        inv_img = cv2.cvtColor(np.array(inv_img), cv2.COLOR_RGB2BGR)
        hsv2 = cv2.cvtColor(inv_img, cv2.COLOR_BGR2HSV)
        lower_val2 = np.array([0, 0, 0]) 
        upper_val2 = np.array([65, 175, 85])
        mask2 = cv2.inRange(hsv2, lower_val2, upper_val2)
        pil_image2 = Image.fromarray(cv2.cvtColor(mask2, cv2.COLOR_BGR2RGB))
        mon_name = pyt.image_to_string(pil_image2, config='--psm 7')
        mon_name = mon_name.capitalize()

    if (mon_name.find('R. ') == 0 or mon_name.find('r. ') in (1, 2)) and ('m' in mon_name or 'n' in mon_name) and 'i' in mon_name and 'e' in mon_name:
        mon_name_readjusted = 'Mr. Mime'
        
    else:
        mon_name_readjusted = re.sub('[^a-zA-Z]', '', mon_name)

    mon_name_readjusted = dfl.get_close_matches(mon_name_readjusted, Gen1_Pokemon, cutoff=0.1)[0]

    scores = []

    move1_score = get_move_score(move1_name, move2_name, move3_name, move4_name, move5_name, mon_name_readjusted, True)
    scores.append((1, move1_name, move1_power, move1_score))
    move2_score = get_move_score(move2_name, move1_name, move3_name, move4_name, move5_name, mon_name_readjusted, True)
    scores.append((2, move2_name, move2_power, move2_score))
    move3_score = get_move_score(move3_name, move1_name, move2_name, move4_name, move5_name, mon_name_readjusted, True)
    scores.append((3, move3_name, move3_power, move3_score))
    move4_score = get_move_score(move4_name, move1_name, move2_name, move3_name, move5_name, mon_name_readjusted, True)
    scores.append((4, move4_name, move4_power, move4_score))
    move5_score = get_move_score(move5_name, move1_name, move2_name, move3_name, move4_name, mon_name_readjusted, False)
    
    scores.sort(key = lambda x: x[3])
    
    if move5_score >= scores[0][3] and scores[0][3] < 2:
        pyd.press('down', scores[0][0] - 1, 0.25)
        pyd.press('z')

    elif move5_score < scores[0][3]:
        pyd.press('x')
    
    elif move5_name in ('PoisonPowder', 'Toxic', 'Will-O-Wisp', 'Glare', 'Stun Spore', 'Thunder Wave', 'GrassWhistle', 
    'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn', 'Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 
    'Sweet Kiss', 'Teeter Dance', 'Leech Seed'):
        found_same = False
        removed = False
        for i in scores:
            if i[1] in ('PoisonPowder', 'Toxic', 'Will-O-Wisp', 'Glare', 'Stun Spore', 'Thunder Wave', 'GrassWhistle', 
            'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn', 'Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 
            'Sweet Kiss', 'Teeter Dance', 'Leech Seed'):
                found_same = True
                if move5_score >= i[3]:
                    removed = True
                    pyd.press('down', i[0] - 1, 0.25)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down', scores[0][0] - 1, 0.25)
                pyd.press('z')
            else:
                pyd.press('x')
        elif removed == False:
            pyd.press('x')
    
    elif move5_power == 0:
        found_same = False
        removed = False
        for i in scores:
            if i[1] not in ('PoisonPowder', 'Toxic', 'Will-O-Wisp', 'Glare', 'Stun Spore', 'Thunder Wave', 'GrassWhistle', 
            'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn', 'Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 
            'Sweet Kiss', 'Teeter Dance', 'Leech Seed') and i[2] == 0:
                found_same = True
                if move5_score >= i[3]:
                    removed = True
                    pyd.press('down', i[0] - 1, 0.25)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down', scores[0][0] - 1, 0.25)
                pyd.press('z')
            else:
                pyd.press('x')
        elif removed == False:
            pyd.press('x')

    else:
        found_same = False
        removed = False
        for i in scores:
            if get_move_type(move5_name) == get_move_type(i[1]) and i[2] > 0:
                found_same = True
                if move5_score >= i[3]:
                    removed = True
                    pyd.press('down', i[0] - 1, 0.25)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down', scores[0][0] - 1, 0.25)
                pyd.press('z')
            else:
                pyd.press('x')
        elif removed == False:
            pyd.press('x')

# atk_mon = attacking Pokemon, def_mon = defending Pokemon
# atk_lvl and def_lvl have to be integers in string form e.g. '50'
def calc_move(atk_mon, atk_lvl, atk_ivs, atk_mon_stages, def_mon, def_lvl, def_ivs, def_mon_stages, reflect_on, lightscreen_on, status_atk, status_def, HP_amount, move, max_min):
    atk_stat1 = str(atk_mon_stages[0])
    spa_stat1 = str(atk_mon_stages[2])
    spe_stat1 = str(atk_mon_stages[4])

    def_stat2 = str(def_mon_stages[1])
    spd_stat2 = str(def_mon_stages[3])
    spe_stat2 = str(def_mon_stages[4])
    
    process = subprocess.check_output(['node', 'PokemonDamageCalculator\Pokemon_Damage_Calculator.mjs', atk_mon, atk_lvl, atk_ivs, atk_stat1, spa_stat1, spe_stat1, def_mon, def_lvl, def_ivs, def_stat2, spd_stat2, spe_stat2, reflect_on, lightscreen_on, status_atk, status_def, HP_amount, move, max_min])
    process = process.decode("utf-8").replace('\n', '').split(' ')
    calcs = []
    for i in range(len(process)):
        if i == 0:
            if math.isnan(float(process[i])):
                calcs.append(0)
            else:
                calcs.append(float(process[i]))
        else:
            calcs.append(int(process[i]))
    # calcs contains (in order): (float) move damage percent (without percentage sign), (int) attacking pokemon speed stat, (int) defending pokemon speed stat
    return calcs

# # print(calc_move('Gengar', 'Chansey', str(50), str(50), 'Fire Punch'))

def continue_text(img, isRGB):
    if isRGB:
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_val = np.array([0, 100, 100])
    upper_val = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_val, upper_val)
    hasRed = np.sum(mask)
    if hasRed > 0:
        return True
    else:
        return False

def edit_image(img):
    img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
    img = img.resize((460, 125))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 255])), axis=-1)
    img[mask] = [0, 0, 0]
    img[~mask] = [255, 255, 255]
    return img

# set text speed to medium
start = time.time()
elapsed = 0
battle = False

while elapsed < 120:
    with mss.mss() as sct:
        battle_start_img = sct.grab((1029, 531, 1747, 655))
        battle_start_img_base = np.array(battle_start_img)
        battle_start_img = edit_image(battle_start_img)
        battle_start = pyt.image_to_string(battle_start_img, lang='FireRedver1')
        battle_start = '\n'.join([line.rstrip() for line in battle_start.splitlines() if line.strip()])
        battle_start = battle_start.capitalize()
        
        if 'would like to battle' in battle_start and get_color(1043, 515) == (200, 168, 72) and get_color(1043, 533) == (40, 80, 104) and continue_text(battle_start_img_base, False):
            which_trainer_img = sct.grab((1029, 531, 1747, 655))
            which_trainer_img = edit_image(which_trainer_img)
            which_trainer = pyt.image_to_string(which_trainer_img, lang='FireRedver1')
            which_trainer = '\n'.join([line.rstrip() for line in which_trainer.splitlines() if line.strip()])
            which_trainer = which_trainer.capitalize()
            if 'Elite' in which_trainer or 'Champion' in which_trainer:
                opp_ivs = '25'
                # opp_ivs = '31'
            else:
                opp_ivs = '9'
                # opp_ivs = '12'
            battle = True
            pyd.press('z')
            break

    elapsed = time.time() - start

tutorial = False
my_mon_struggle = False
prev_opp_faint = False
make_move = False
new_my_mon = True
new_opp_mon = True
switch_mon = False
make_switch = False
no_switch = False
fight = False
my_mon_faint = False
my_actual_move = ''
no_my_stat_change = False
no_stat_change = False
no_new_moves = False
KeepMon = False
reflect_on = 'false'
lightscreen_on = 'false'
starting = True
KeepSeed = False
drop_attack = False
opp_drop_attack = False

while battle:
    if starting:
        while get_color(1491, 516) != (208, 160, 208):
            with mss.mss() as sct:
                battle_start_img_base = np.array(sct.grab((1010, 510, 1890, 670)))
                battle_start_img = sct.grab((1029, 531, 1747, 655))
                battle_start_img = edit_image(battle_start_img)
                battle_start = pyt.image_to_string(battle_start_img, lang='FireRedver1')
                battle_start = '\n'.join([line.rstrip() for line in battle_start.splitlines() if line.strip()])
                battle_start = battle_start.capitalize()

            if battle_start.find('Foe') == 0 and 'cuts' in battle_start and 'attack' in battle_start:
                drop_attack = True
            elif battle_start.find('Foe') != 0 and 'cuts' in battle_start and 'attack' in battle_start:
                opp_drop_attack = True

            if get_color(1026, 579) == (160, 208, 224) and get_color(1873, 579) == (160, 208, 224) and continue_text(battle_start_img_base, False):
                tutorial = True
                pyd.press('z')

        starting = False

    if get_color(1491, 516) == (208, 160, 208) and make_switch == False:
        make_move = True

        if new_my_mon == True and switch_mon == False:
            my_mon = get_pokemon_name('plyr')
            my_mon_lvl = get_pokemon_level('plyr')
            if no_my_stat_change == False:
                my_stat_stages = [0, 0, 0, 0, 0]
            my_accuracy = 0
            my_status = ''
            check_status_move = False
            prev_move = 0
            disabled_move = ''
            make_switch = False
            PerishSong = False
            PerishCount = 0
            my_mon_confused = False
            new_my_mon = False
            Taunt = False
            TauntCount = 0
            Torment = False
            Encore = False
            
            if drop_attack == True: # and (already_out == False or my_mon_faint == False) and switch_mon == False
                my_stat_stages[0] -= 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
            drop_attack = False

        if new_opp_mon == True:
            if KeepMon == False:
                opp_mon = get_pokemon_name('opp')
            opp_mon_lvl = get_pokemon_level('opp')
            if no_stat_change == False:
                opp_stat_stages = [0, 0, 0, 0, 0]
            if no_new_moves == False:
                actual_moves = []
                move_added = False
            opp_status = ''
            check_status_move = False
            opp_mon_confused = False
            if KeepSeed == False:
                LeechSeed = False
            new_opp_mon = False
            opp_switch = False
            opp_moves = get_moveset(opp_mon, int(opp_mon_lvl))
            opp_mon_faint = False

            if opp_drop_attack == True:
                opp_stat_stages[0] -= 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
            opp_drop_attack = False

        no_my_stat_change = False
        no_stat_change = False
        no_new_moves = False
        KeepMon = False

        if opp_mon in ('Diglett', 'Dugtrio') and ('Flying' not in get_mon_type(my_mon) or my_mon not in ('Gastly', 'Haunter', 'Gengar')):
            no_switch = True
            make_switch = False

        if my_mon_lvl == 'empty' or opp_mon_lvl == 'empty':
            if my_mon_lvl == 'empty' and opp_mon_lvl != 'empty':
                my_mon_lvl = opp_mon_lvl
            elif my_mon_lvl != 'empty' and opp_mon_lvl == 'empty':
                opp_mon_lvl = my_mon_lvl
            elif my_mon_lvl == 'empty' and opp_mon_lvl == 'empty':
                my_mon_lvl = '30'
                opp_mon_lvl = '30'
        
        # check status conditions
        which_my_status = get_color(1537, 457)
        if which_my_status == (224, 112, 80):
            my_status = 'brn'
        elif which_my_status == (136, 176, 224):
            my_status = 'frz'
        elif which_my_status == (192, 96, 192):
            my_status = 'psn'
        elif which_my_status == (184, 184, 24):
            my_status = 'par'
        elif which_my_status == (160, 160, 136):
            my_status = 'slp'
        else:
            my_status = ''

        which_opp_status = get_color(1079, 208)
        if which_opp_status == (224, 112, 80):
            opp_status = 'brn'
        elif which_opp_status == (136, 176, 224):
            opp_status = 'frz'
        elif which_opp_status == (192, 96, 192):
            opp_status = 'psn'
        elif which_opp_status == (184, 184, 24):
            opp_status = 'par'
        elif which_opp_status == (160, 160, 136):
            opp_status = 'slp'
        else:
            opp_status = ''

        opp_HP = get_pokemon_HP('opp')

        opp_dmgs = []
        for i in range(len(opp_moves)):
            opp_dmgs.append((opp_moves[i], calc_move(opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, my_mon, my_mon_lvl, '31', my_stat_stages, reflect_on, lightscreen_on, opp_status, my_status, str(opp_HP), opp_moves[i], 'max')[0]))
        
        opp_dmgs.sort(key = lambda x: x[1], reverse = True)

        opp_move_name = opp_dmgs[0][0]
        opp_move_name = dfl.get_close_matches(opp_move_name, Gens1to3_Moves, cutoff=0.1)[0]

        opp_move_dmg = opp_dmgs[0][1]

        calc_info = calc_move(opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, my_mon, my_mon_lvl, '31', my_stat_stages, reflect_on, lightscreen_on, opp_status, my_status, str(opp_HP), opp_moves[0], 'max')
        
        if move_added and len(actual_moves) > 0:
            opp_actual_moves_dmgs = []
            for i in range(len(actual_moves)):
                opp_actual_moves_dmgs.append((actual_moves[i], calc_move(opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, my_mon, my_mon_lvl, '31', my_stat_stages, reflect_on, lightscreen_on, opp_status, my_status, str(opp_HP), actual_moves[i], 'max')[0]))
            
            opp_actual_moves_dmgs.sort(key = lambda x: x[1], reverse = True)

            opp_actual_move_dmg = opp_actual_moves_dmgs[0][1]

            if opp_actual_move_dmg > opp_move_dmg or len(actual_moves) == 4:
                opp_move_name = opp_actual_moves_dmgs[0][0]
                opp_move_dmg = opp_actual_move_dmg

        move_added = False

        my_HP = get_pokemon_HP('plyr')
        # print('my HP:' + str(my_HP))
        # print('opp highest dmg move:' + opp_move_name + ': ' + str(opp_move_dmg))
        if my_mon_struggle == True and no_switch == False:
            new_opp_mon = False
            make_switch = True

        elif no_switch:
            fight = True
            print('no switching')
            if Encore:
                pyd.press('z')

            else:
                pyd.press('z')
                time.sleep(0.25)
                if get_color(1482, 583) in ((40, 80, 104), (40, 79, 103)):
                    time.sleep(2)
                with mss.mss() as sct:
                    no_moves_img = sct.grab((1029, 531, 1747, 655))
                    no_moves_img = edit_image(no_moves_img)

                no_moves = pyt.image_to_string(no_moves_img, lang='FireRedver1')
                no_moves = '\n'.join([line.rstrip() for line in no_moves.splitlines() if line.strip()])
                no_moves = no_moves.capitalize()
                    
                if no_moves.find('Foe') != 0 and 'moves left' in no_moves:
                    my_mon_struggle = True
                    my_actual_move = ''
                else:
                    my_moves = []
                    for i in range(1, 5):
                        move = get_pokemon_move(i)
                        if move != 'empty':
                            my_moves.append(move)
                        
                    usable_moves = []
                    for i in range(len(my_moves)):
                        usable_moves.append((my_moves[i][0], my_moves[i][1], calc_move(my_mon, my_mon_lvl, '31', my_stat_stages, opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, reflect_on, lightscreen_on, my_status, opp_status, str(my_HP), my_moves[i][1], 'min')[0]))
                        
                    usable_moves.sort(key = lambda x: x[2], reverse = True)
                    
                    for i in range(len(usable_moves)):
                        move_to_use = usable_moves[i]
                        my_move_name = move_to_use[1]
                        select_move(move_to_use[0])
                        if get_color(1631, 568) == (232, 1, 1) or get_move_accuracy(my_move_name) < 70 or (my_move_name == my_actual_move
                        and Torment == True) or (my_move_name in (disabled_move, 'Selfdestruct', 'Explosion') and 
                        (opp_move_dmg/my_HP < 1 or usable_moves[min(i+1, len(usable_moves)-1)][2]/opp_HP >= 1)) or my_move_name == 'Focus Punch' \
                        or (get_move_type(my_move_name) == 'Water' and opp_mon == 'Lapras') or (get_move_type(my_move_name) == 'Fire' 
                        and opp_mon in ('Growlithe', 'Arcanine', 'Ponyta', 'Rapidash')) or (move_to_use[1] in ('Hyper Voice', 'Uproar') 
                        and opp_mon in ('Voltorb', 'Electrode', 'Mr. Mime')) or (move_to_use[1] in ('Bounce', 'Dig', 'Dive', 'Fly', 
                        'Razor Wind', 'Skull Bash', 'Sky Attack', 'SolarBeam') and PerishCount <= 2 and PerishSong):
                            pass
                        else:
                            break
                    
                    if get_color(1631, 568) == (232, 1, 1) or my_move_name == disabled_move:
                        for i in range(len(usable_moves)):
                            move_to_use = usable_moves[i]
                            my_move_name = move_to_use[1]
                            select_move(move_to_use[0])
                            if get_color(1631, 568) == (232, 1, 1) or my_move_name == disabled_move or (my_move_name == my_actual_move and Torment == True):
                                pass
                            else:
                                break    
                    
                    my_actual_move = my_move_name

            pyd.press('z')

        # Switch when my mon is in crit range and the opposing mon outspeeds
        elif make_switch == False and ((opp_move_dmg/my_HP >= 0.5 and calc_info[1] >= calc_info[2]) 
        or my_accuracy <= -3 or PerishCount == 3 or my_status == 'frz' or (my_HP < 40 and my_mon_confused == True)):
            make_switch = True
            fight = False
            # print(my_mon_lvl, opp_mon_lvl)

        # If opp KOs but my mon outspeeds check whether my mon KOs
        elif make_switch == False:
            fight = True
            
            if Encore:
                my_move_calc = calc_move(my_mon, my_mon_lvl, '31', my_stat_stages, opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, reflect_on, lightscreen_on, my_status, opp_status, str(my_HP), my_actual_move, 'min')
                if (my_move_calc[0]/opp_HP >= 1 and calc_info[1] < calc_info[2]) or (my_move_calc[0] > 0 and opp_move_dmg/my_HP <= 0.5):
                    pyd.press('z', 2, 0.25)

                else:
                    make_switch = True

            else:
                pyd.press('z')
                time.sleep(0.25)
                if get_color(1482, 583) in ((40, 80, 104), (40, 79, 103)):
                    time.sleep(2)
                with mss.mss() as sct:
                    no_moves_img = sct.grab((1029, 531, 1747, 655))
                    no_moves_img = edit_image(no_moves_img)
                no_moves = pyt.image_to_string(no_moves_img, lang='FireRedver1')
                no_moves = '\n'.join([line.rstrip() for line in no_moves.splitlines() if line.strip()])
                no_moves = no_moves.capitalize()
                
                if no_moves.find('Foe') != 0 and 'moves left' in no_moves:
                    my_mon_struggle = True
                    new_my_mon = False
                    my_actual_move = ''
                    pyd.press('z')

                else:
                    my_moves = []
                    for i in range(1, 5):
                        move = get_pokemon_move(i)
                        if move != 'empty':
                            my_moves.append(move)
                        
                    if len(my_moves) == 0:
                        make_switch = True

                    if make_switch == False:
                        usable_moves = []
                        for i in range(len(my_moves)):
                            usable_moves.append((my_moves[i][0], my_moves[i][1], calc_move(my_mon, my_mon_lvl, '31', my_stat_stages, opp_mon, opp_mon_lvl, opp_ivs, opp_stat_stages, reflect_on, lightscreen_on, my_status, opp_status, str(my_HP), my_moves[i][1], 'min')[0]))
                            
                        usable_moves.sort(key = lambda x: x[2], reverse = True)
                    # print(usable_moves)
                    # print(my_moves)
                    # print(my_mon_lvl)
                    # print(opp_mon_lvl)
                    # Get strongest move that does damage and has pp
                    # look for status inflicting moves (50/50 between status inflict and status change if have both)
                    # if usable status inflict moves and usable status moves have a length greater than one 50/50
                    # if no status inflict -> go to status moves and same thing the other way
                    # if no potential status moves -> go to inflict status
                    # check status move only false for status move and not status inflict moves
                    
                        for i in range(len(usable_moves)):
                            move_to_use = usable_moves[i]
                            my_move_name = move_to_use[1]
                            select_move(move_to_use[0])
                            if get_color(1631, 568) == (232, 1, 1) or get_move_accuracy(my_move_name) < 70 or (my_move_name == my_actual_move
                            and Torment == True) or my_move_name in (disabled_move, 'Selfdestruct', 'Explosion', 'Focus Punch') \
                            or (get_move_type(my_move_name) == 'Water' and opp_mon == 'Lapras') or (get_move_type(my_move_name) == 'Fire' 
                            and opp_mon in ('Growlithe', 'Arcanine', 'Ponyta', 'Rapidash')) or (move_to_use[1] in ('Hyper Voice', 'Uproar') 
                            and opp_mon in ('Voltorb', 'Electrode', 'Mr. Mime')) or (move_to_use[1] in ('Bounce', 'Dig', 'Dive', 'Fly', 
                            'Razor Wind', 'Skull Bash', 'Sky Attack', 'SolarBeam') and PerishCount <= 2 and PerishSong):
                                # print(my_move_name + ' is not usable')
                                if i == len(usable_moves) - 1:
                                    make_switch = True
                                    break
                                else:
                                    pass
                            elif my_move_name in ('Recover', 'Morning Sun', 'Synthesis', 'Moonlight') and my_HP <= 50 and opp_move_dmg < 50  and Taunt == False:
                                break
                            elif move_to_use[2] == 0:
                                if opp_status == '' and opp_mon not in ('Rattata', 'Raticate', 'Machop', 'Machoke', 'Machamp', 'Dratini', 'Dragonair') and Taunt == False:
                                    if my_move_name in ('PoisonPowder', 'Toxic') and 'Steel' not in get_mon_type(opp_mon) and 'Poison' not in get_mon_type(opp_mon):
                                        break
                                    elif my_move_name == 'Will-O-Wisp' and 'Fire' not in get_mon_type(opp_mon):
                                        break
                                    elif my_move_name in ('Glare', 'Stun Spore', 'Thunder Wave') and opp_mon not in ('Persian', 'Hitmonlee', 'Ditto'):
                                        break
                                    elif my_move_name == 'Thunder Wave' and 'Ground' not in get_mon_type(opp_mon):
                                        break
                                    elif my_move_name in ('GrassWhistle', 'Sing') and opp_mon not in ('Drowzee', 'Hypno', 'Voltorb', 'Electrode', 'Mr. Mime'):
                                        break
                                    elif my_move_name in ('GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn') and opp_mon not in ('Drowzee', 'Hypno'):
                                        break
                                if opp_mon_confused == False and Taunt == False:
                                    if my_move_name == 'Supersonic' and opp_mon not in ('Voltorb', 'Electrode', 'Mr. Mime', 'Slowpoke', 'Slowbro', 'Lickitung'):
                                        break
                                    elif my_move_name in ('Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance') and opp_mon not in ('Slowpoke', 'Slowbro', 'Lickitung'):
                                        break
                                if my_move_name == 'Leech Seed' and LeechSeed == False and 'Grass' not in get_mon_type(opp_mon) and Taunt == False:
                                        break
                                else:
                                    make_switch = True
                                    break
                            else:
                                break
                        # print(move_to_use)
                        my_actual_move = my_move_name
                    # Get status moves
                    if make_switch == False and my_move_name not in ('Recover', 'Morning Sun', 'Synthesis', 'Moonlight') and opp_move_dmg/my_HP <= (1/3) and move_to_use[2]/opp_HP < 0.5 and int(opp_mon_lvl) >= int(my_mon_lvl) and Taunt == False:
                        # print('checking status moves')
    # toxic, paralysis, leech seed, sleep, burn, poison, confusion, + move accuracy
                        potential_status_inflict = []
                        if opp_status == '' and opp_mon_confused == False and LeechSeed == False:
                            for i in range(len(usable_moves)):
                                status_inflict_move = usable_moves[i]
                                select_move(status_inflict_move[0])
                                if get_color(1631, 568) == (232, 1, 1) or get_move_accuracy(status_inflict_move[1]) <= 70 or (status_inflict_move[1] == my_actual_move and Torment == True):
                                    pass
                                elif (opp_status != '' or opp_mon in ('Rattata', 'Raticate', 'Machop', 'Machoke', 'Machamp', 'Dratini', 'Dragonair')) and \
                                status_inflict_move[1] in ('PoisonPowder', 'Toxic', 'Will-O-Wisp', 'Glare', 'Stun Spore', 'Thunder Wave', 
                                'GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn', 'Confuse Ray', 'Flatter', 
                                'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance', 'Leech Seed'):
                                    pass
                                elif (status_inflict_move[1] in ('PoisonPowder', 'Toxic') and 'Steel' in get_mon_type(opp_mon) and 
                                'Poison' in get_mon_type(opp_mon)) or (status_inflict_move[1] == 'Will-O-Wisp' and 'Fire' 
                                in get_mon_type(opp_mon)) or (status_inflict_move[1] == 'Thunder Wave' and 'Ground' 
                                in get_mon_type(opp_mon)):
                                    pass
                                elif (status_inflict_move[1] in ('Glare', 'Stun Spore', 'Thunder Wave') and opp_mon in 
                                ('Persian', 'Hitmonlee', 'Ditto')) or (status_inflict_move[1] in 
                                ('GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn') and 
                                opp_mon in ('Drowzee', 'Hypno')) or (status_inflict_move[1] in ('GrassWhistle', 'Sing') 
                                and opp_mon in ('Voltorb', 'Electrode', 'Mr. Mime')):
                                    pass
                                elif (status_inflict_move[1] in ('Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance')
                                and (opp_mon in ('Slowpoke', 'Slowbro', 'Lickitung') or opp_mon_confused == True)) or (status_inflict_move[1] == 'Supersonic' 
                                and opp_mon in ('Voltorb', 'Electrode', 'Mr. Mime')):
                                    pass
                                elif status_inflict_move[1] == 'Leech Seed' and (LeechSeed == True or 'Grass' in get_mon_type(opp_mon)):
                                    pass
                                elif status_inflict_move[1] in ('PoisonPowder', 'Toxic', 'Will-O-Wisp', 'Glare', 
                                'Stun Spore', 'Thunder Wave', 'GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 
                                'Yawn', 'Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance', 'Leech Seed'):
                                    potential_status_inflict.append((status_inflict_move[0], status_inflict_move[1]))
                        if len(potential_status_inflict) > 0:
                            usable_status_inflict = []
                            for i in potential_status_inflict:
                                if i[1] == 'Toxic':
                                    usable_status_inflict.append(i[0], i[1], 3 + get_move_accuracy(i[1]))
                                elif i[1] in ('Glare', 'Stun Spore', 'Thunder Wave'):
                                    usable_status_inflict.append(i[0], i[1], 2.5 + get_move_accuracy(i[1]))
                                elif i[1] == 'Leech Seed':
                                    usable_status_inflict.append(i[0], i[1], 2 + get_move_accuracy(i[1]))
                                elif i[1] in ('GrassWhistle', 'Hypnosis', 'Lovely Kiss', 'Sing', 'Sleep Powder', 'Spore', 'Yawn'):
                                    usable_status_inflict.append(i[0], i[1], 1.5 + get_move_accuracy(i[1]))
                                elif i[1] == 'Will-O-Wisp':
                                    usable_status_inflict.append(i[0], i[1], 1 + get_move_accuracy(i[1]))
                                elif i[1] == 'PoisonPowder':
                                    usable_status_inflict.append(i[0], i[1], 0.5 + get_move_accuracy(i[1]))
                                elif i[1] in ('Confuse Ray', 'Flatter', 'Supersonic', 'Swagger', 'Sweet Kiss', 'Teeter Dance'):
                                    usable_status_inflict.append(i[0], i[1], get_move_accuracy(i[1]))
                        potential_status_moves = []
                        if check_status_move == False:
                            for i in range(len(usable_moves)):
                                move_to_use2 = usable_moves[i]
                                select_move(move_to_use2[0])
                                if get_color(1631, 568) == (232, 1, 1) or (move_to_use2 == my_actual_move and Torment == True) or \
                                move_to_use2[1] in (disabled_move, 'Memento') or (move_to_use2[1] == 'Curse' and 'Ghost' 
                                in get_mon_type(my_mon)) or ((move_to_use2[1] in ('Growl', 'Metal Sound', 'Screech') and opp_mon 
                                in ('Voltorb', 'Electrode', 'Mr. Mime'))):
                                    pass
                                elif move_to_use2[2] == 0 and move_to_use2[1] in status_moves:
                                    potential_status_moves.append((move_to_use2[0], move_to_use2[1]))
                        if len(potential_status_moves) > 0:
                            usable_status_moves = []
                            for i in potential_status_moves:
                                if len(status_moves[i[1]]) == 3:
                                    if ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][2] == 'target') or
                                    (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][2] == 'user')) and \
                                    get_move_type(opp_move_name) in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1]))
                                    
                                    elif ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][2] == 'target') or
                                    (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][2] == 'user')) and \
                                    get_move_type(opp_move_name) not in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1]))

                                    elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][2] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][2] == 'target')) and \
                                    get_move_type(my_move_name) in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1]))
                                    
                                    elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][2] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][2] == 'target')) and \
                                    get_move_type(my_move_name) not in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1]))

                                    elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spe' and status_moves[i[1]][2] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spe' and status_moves[i[1]][2] == 'target')) and calc_info[1] >= calc_info[2]:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1]))
                                        
                                elif len(status_moves[i[1]]) == 5:
                                    if ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][4] == 'target') or
                                    (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][4] == 'user')) and \
                                    get_move_type(opp_move_name) in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1], status_moves[i[1]][2], status_moves[i[1]][3]))
                                    
                                    elif ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][4] == 'target') or
                                    (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][4] == 'user')) and \
                                    get_move_type(opp_move_name) not in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1], status_moves[i[1]][2], status_moves[i[1]][3]))

                                    elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][4] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][4] == 'target')) and \
                                    get_move_type(my_move_name) in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1], status_moves[i[1]][2], status_moves[i[1]][3]))
                                    
                                    elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][4] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][4] == 'target')) and \
                                    get_move_type(my_move_name) not in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1], status_moves[i[1]][2], status_moves[i[1]][3]))
                                else:
                                    if ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][6] == 'user') or
                                    (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][6] == 'target')) and \
                                    get_move_type(my_move_name) in physical_types:
                                        usable_status_moves.append((i[0], i[1], status_moves[i[1]][0], status_moves[i[1]][1], status_moves[i[1]][2], status_moves[i[1]][3], status_moves[i[1]][4], status_moves[i[1]][5]))
                        else:
                            check_status_move = True

                        if len(potential_status_inflict) > 0 and len(usable_status_inflict) > 0 and len(potential_status_moves) > 0 and len(usable_status_moves) > 0:
                            use_which_status = random.randint(1, 2)
                            if use_which_status == 1:
                                usable_status_inflict.sort(key = lambda x: x[2], reverse = True)
                                my_actual_move = usable_status_inflict[0][1]
                                select_move[usable_status_inflict[0][0]]
                            else:
                                usable_status_moves.sort(key = lambda x: (len(x), abs(x[2])), reverse = True)
                                my_actual_move = usable_status_moves[0][1]
                                select_move(usable_status_moves[0][0])
                                check_status_move = True
                        elif len(potential_status_inflict) > 0 and len(usable_status_inflict) > 0:
                            usable_status_inflict.sort(key = lambda x: x[2], reverse = True)
                            my_actual_move = usable_status_inflict[0][1]
                            select_move[usable_status_inflict[0][0]]
                        elif len(potential_status_moves) > 0 and len(usable_status_moves) > 0:
                            usable_status_moves.sort(key = lambda x: (len(x), abs(x[2])), reverse = True)
                            my_actual_move = usable_status_moves[0][1]
                            select_move(usable_status_moves[0][0])
                            check_status_move = True
                        else:
                            select_move(move_to_use[0])
                    # get status move with the largest decrease or increase based on the opponents move or my move
                    
                    if make_switch == False and ((move_to_use[2]/opp_HP >= 1 and calc_info[1] < calc_info[2]) or (opp_move_dmg/my_HP <= 0.5)):
                        # print('attack')
                        switch_mon = False
                        pyd.press('z')
                    
                    else:
                        make_switch = True

    if make_switch == True and no_switch == False:
        if get_color(1491, 516) == (208, 160, 208):
            if fight == False:
                pyd.press('down')
                pyd.press('z')
            else:
                pyd.press('x')
                time.sleep(0.1)
                pyd.press('down')
                pyd.press('z')
            
        time.sleep(2.5)
        
        while tutorial and get_color(1026, 579) == (160, 208, 224) and get_color(1873, 579) == (160, 208, 224):
            pyd.press('z')
            time.sleep(1)

        move_type = get_move_type(opp_move_name)
        party = get_party_status()
        updated_party = []
        def_type_relations = []
        off_type_relations = []
        send_out = ''

        if len(party) == 0:
            no_switch = True
        
        else:
            for i in range(len(party)):
                for t in get_mon_type(party[i][1]):
                    def_type_relations.append(get_type_relation(t, move_type))
                    for j in get_mon_type(opp_mon):
                        off_type_relations.append(get_type_relation(j, t))
                # print(def_type_relations)
                if len(def_type_relations) == 2:
                    def_effectiveness = def_type_relations[0] * def_type_relations[1]
                else:
                    def_effectiveness = def_type_relations[0]
                if len(off_type_relations) == 1:
                    off_effectiveness = off_type_relations[0]
                    off_effectiveness2 = -1
                elif len(off_type_relations) == 2:
                    off_effectiveness = off_type_relations[0] * off_type_relations[1]
                    off_effectiveness2 = -1
                else:
                    off_effectiveness = off_type_relations[0] * off_type_relations[1]
                    off_effectiveness2 = off_type_relations[2] * off_type_relations[3]

                updated_member = party[i][0], party[i][1], party[i][2], def_effectiveness, off_effectiveness, off_effectiveness2
                updated_party.append(updated_member)
                def_type_relations = []
                off_type_relations = []

            updated_party.sort(key = lambda x: (x[3], -(x[4]), -(x[5]), -(x[2])))
            # print(updated_party)
            # switch in pokemon that best takes the move typing
            # no switch if all of my pokemon are at most neutral 1 to the attack and are below 50% HP
            # no switch if all of my pokemon resist attack 0.5 or 0 and are below 25% HP
            # no switch if all of my pokemon's types are resisted by the opposing pokemon
            # switch in if at least neutral or super effective
            for i in range(len(updated_party)):
                if my_mon_faint == True:
                    send_out = updated_party[i][0]
                    break
                elif updated_party[i][3] <= 0.5 and updated_party[i][2] > 25:
                    if updated_party[i][4] >= 1 or updated_party[i][5] >= 1:
                        send_out = updated_party[i][0]
                        break
                elif updated_party[i][3] == 1 and updated_party[i][2] > 50:
                    if updated_party[i][4] >= 1 or updated_party[i][5] >= 1:
                        send_out = updated_party[i][0]
                        break

            if send_out == '':
                no_switch = True

        # when have to switch in pokemon after being koed
        if my_mon_faint == True:
            new_my_mon = True
            my_mon_faint = False
            my_stat_stages = [0, 0, 0, 0, 0]
            no_my_stat_change = True
            make_move = True
            my_actual_move = ''

            if opp_mon_faint == True:
                if no_stat_change == False:
                    opp_stat_stages = [0, 0, 0, 0, 0]
                    no_stat_change = True
                    no_new_moves = False

            pyd.press('down', int(send_out[-1]) - 1, 0.25)
            pyd.press('z')
            pyd.press('z')

        elif no_switch == False:
            my_mon_struggle = False
            new_my_mon = True
            switch_mon = True
            make_move = True
            my_actual_move = ''
            pyd.press('down', int(send_out[-1]) - 1, 0.25)
            pyd.press('z')
            pyd.press('z')

        else:
            make_move = False
            pyd.press('x')
            time.sleep(2)
            pyd.press('up')

        # if my_mon_faint == False:
        #     make_switch = False
        
        make_switch = False
        fight = False

    #check if pokemon is still fighting
    if make_move == True:
        opp_move_used = []
        opp_last_move = ''
        my_move_used = None
        my_move_first = False
        which_turn = 0
        if switch_mon:
            my_move_first = True
            which_turn = 1
        opp_move_first = False
        my_stat_changed = False
        opp_made_switch = False
        prev_opp_faint = False
        prev_text_length = 100
        start = time.time()
        elapsed = 0

        # disabled red arrow
        while elapsed < 5 or (get_color(1043, 515) in ((200, 168, 72), (198, 166, 71)) and get_color(1043, 533) in ((40, 80, 104), (40, 79, 103)) and get_color(1491, 516) != (208, 160, 208)):
            already_add = False

            lvl_box = get_color(1583, 303)

            while tutorial and get_color(1026, 579) == (160, 208, 224) and get_color(1873, 579) == (160, 208, 224):
                with mss.mss() as sct:
                    battle_start_img_base = np.array(sct.grab((1010, 510, 1890, 670)))
                if continue_text(battle_start_img_base, False):
                    pyd.press('z')
    
            # move_used_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
            with mss.mss() as sct:
                move_used_img = sct.grab((1029, 531, 1747, 655))
                move_used_img_base = np.array(move_used_img)
                move_used_img = edit_image(move_used_img)
            move_used = pyt.image_to_string(move_used_img, lang='FireRedver1')
            move_used = '\n'.join([line.rstrip() for line in move_used.splitlines() if line.strip()])
            move_used = move_used.capitalize()
            
            if len(move_used) < prev_text_length:
                different_text = True
            
            prev_text_length = len(move_used)

            if different_text:
                if move_used.find('Foe') == 0 and 'cuts' in move_used and 'attack' in move_used:
                    my_stat_stages[0] -= 1
                    my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                    different_text = False

                elif move_used.find('Foe') != 0 and 'cuts' in move_used and 'attack' in move_used:
                    opp_stat_stages[0] -= 1
                    opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                    different_text = False

                elif move_used.find('Foe') == 0 and 'raised' in move_used and 'speed' in move_used:
                    opp_stat_stages[4] += 1
                    opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
                    different_text = False

                elif move_used.find('Foe') != 0 and 'raised' in move_used and 'speed' in move_used:
                    my_stat_stages[4] += 1
                    my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
                    different_text = False

                elif move_used.find('Foe') != 0 and ((('can’t' in move_used or 'can\'t' in move_used) and (' move!' in move_used 
                or ' move !' in move_used)) or ('is fast' in move_used) or (' is' in move_used and ('frozen' in move_used or 'solid' 
                in move_used)) or ('flinched' in move_used) or ('recharge' in move_used) and ('by love' in move_used)):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        my_move_first = False
                    else:
                        my_move_first = True
                    my_move_used = False
                    if Taunt:
                        TauntCount += 1
                    if PerishSong:
                        PerishCount += 1
                    different_text = False
                    just_sent_out = False

                elif move_used.find('Foe') != 0 and 'moves left' in move_used and continue_text(move_used_img_base, False):
                    my_mon_struggle = True
                    my_actual_move = ''
                    pyd.press('z')

                elif move_used.find('Foe') != 0 and ('sprang up' in move_used or 'dug a hole' in move_used or (' hid' in move_used 
                and 'underwater' in move_used) or (' flew' in move_used and ' high' in move_used) or (' up ' in move_used and 
                'whirlwind' in move_used) or ('lowered' in move_used and 'head' in move_used) or ('glowing' in move_used) or 
                (' took' in move_used and 'sunlight' in move_used)):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        my_move_first = False
                    else:
                        my_move_first = True
                    if Taunt:
                        TauntCount += 1
                    if PerishSong:
                        PerishCount += 1
                    different_text = False
                    just_sent_out = False
                    # print('2 turn move used')

                elif move_used.find('Foe') != 0 and 'snapped' in move_used and 'out' in move_used:
                    my_mon_confused = False
                    different_text = False
                    just_sent_out = False

                elif move_used.find('Foe') != 0 and 'confused' in move_used:
                    my_mon_confused = True
                    different_text = False
                    just_sent_out = False
                    if ' is' in move_used:
                        start2 = time.time()
                        elapsed2 = 0
                        while elapsed2 < 3:
                            # confused_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
                            with mss.mss() as sct:
                                confused_img = sct.grab((1029, 531, 1747, 655))
                            # confused_img = np.array(confused_img)
                            confused_img = edit_image(confused_img)
                            confused = pyt.image_to_string(confused_img, lang='FireRedver1')
                            confused = '\n'.join([line.rstrip() for line in confused.splitlines() if line.strip()])
                            confused = confused.capitalize()

                            if len(confused) < prev_text_length:
                                different_text = True
                            
                            prev_text_length = len(confused)

                            if ' hurt' in confused:
                                which_turn += 1
                                if which_turn % 2 == 0:
                                    my_move_first = False
                                else:
                                    my_move_first = True
                                my_move_used = False
                                if Taunt:
                                    TauntCount += 1
                                if PerishSong:
                                    PerishCount += 1
                                break
                            elif len(confused) >= 7:
                                break
                            elapsed2 = time.time() - start2

                elif move_used.find('Foe') != 0 and 'used' in move_used:
                    which_turn += 1
                    if which_turn % 2 == 0:
                        my_move_first = False
                    else:
                        my_move_first = True
                    if Taunt:
                        TauntCount += 1
                    if PerishSong:
                        PerishCount += 1
                    different_text = False
                    just_sent_out = False
                    start2 = time.time()
                    elapsed2 = 0
                    while elapsed2 < 3:
                        # my_move_missed_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
                        with mss.mss() as sct:
                            my_move_missed_img = sct.grab((1029, 531, 1747, 655))
                        # my_move_missed_img = np.array(my_move_missed_img)
                        my_move_missed_img = edit_image(my_move_missed_img)
                        my_move_missed = pyt.image_to_string(my_move_missed_img, lang='FireRedver1')
                        my_move_missed = '\n'.join([line.rstrip() for line in my_move_missed.splitlines() if line.strip()])
                        my_move_missed = my_move_missed.capitalize()

                        if len(my_move_missed) < prev_text_length:
                            different_text = True
                        
                        prev_text_length = len(my_move_missed)
                        
                        if (my_move_missed.find('Foe') == 0 and (' use' in my_move_missed or ' is ' in my_move_missed 
                        or ' was ' in my_move_missed or ' has ' in my_move_missed or 'flinch' in my_move_missed)) or 'potion' \
                        in my_move_missed or 'full restore' in my_move_missed:
                            break

                        elif my_move_missed.find('Foe') == 0 and ('sprang up' in my_move_missed or 'dug a hole' in my_move_missed or (' hid' in my_move_missed 
                        and 'underwater' in my_move_missed) or (' flew' in my_move_missed and ' high' in my_move_missed) or (' up ' in my_move_missed and 
                        'whirlwind' in my_move_missed) or ('lowered' in my_move_missed and 'head' in my_move_missed) or ('glowing' in my_move_missed) or 
                        (' took' in my_move_missed and 'sunlight' in my_move_missed)):
                            which_turn += 1
                            if which_turn % 2 == 0:
                                opp_move_first = False
                            else:
                                opp_move_first = True
                            different_text = False
                            break

                        elif my_move_missed.find('Foe') != 0 and 'disabled' in my_move_missed and 'no more' in my_move_missed:
                            disabled_move = ''
                            break
                
                        elif my_move_missed.find('Foe') != 0 and 'was freed' in my_move_missed:
                            no_switch = False
                            make_switch = False
                            for i in opp_move_used:
                                if i[0] in ('Bind', 'Clamp', 'Fire Spin', 'Sand Tomb', 'Whirlpool', 'Wrap') and 'NoAdd' not in i:
                                    i.append('NoAdd')
                            different_text = False

                        elif 'reflect' in my_move_missed and 'wore off' in my_move_missed:
                            reflect_on = 'false'
                            break

                        elif 'light screen' in my_move_missed and 'wore off' in my_move_missed:
                            lightscreen_on = 'false'
                            break
                        
                        elif 'no longer' in my_move_missed and 'protected' in my_move_missed:
                            Safeguard = False
                            break

                        elif 'encore' in my_move_missed and 'ended' in my_move_missed:
                            Encore = False
                            break

                        elif 'missed' in my_move_missed or 'evaded' in my_move_missed or 'prevents' in my_move_missed or \
                        'failed' in my_move_missed or 'blocks' in my_move_missed or (('doesn’t' in my_move_missed or 'doesn\'t' 
                        in my_move_missed)) and 'affect' in my_move_missed or (' no ' in my_move_missed and 'target' in 
                        my_move_missed) or (my_move_missed.find('Foe') == 0 and 'protected' in my_move_missed): 
                            if my_move_used == None:
                                my_move_used = False
                                already_add = True
                            break

                        elif 'fell!' in my_move_missed or 'rose!' in my_move_missed or 'fell !' in my_move_missed or 'rose !' in my_move_missed:
                            if my_move_used == None:
                                my_move_used = True
                                my_stat_changed = True
                                already_add = True
                            break
                        
                        elif 'fainted' in my_move_missed:
                            break

                        elapsed2 = time.time() - start2

                    if my_move_used == None:
                        my_move_used = True

                elif move_used.find('Foe') != 0 and 'was freed' in move_used:
                    no_switch = False
                    make_switch = False
                    for i in opp_move_used:
                        if i[0] in ('Bind', 'Clamp', 'Fire Spin', 'Sand Tomb', 'Whirlpool', 'Wrap') and 'NoAdd' not in i:
                            i.append('NoAdd')
                    different_text = False
                    # print('freed')

                elif move_used.find('Foe') != 0 and 'is disabled' in move_used and continue_text(move_used_img_base, False):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        my_move_first = False
                    else:
                        my_move_first = True
                    if Taunt:
                        TauntCount += 1
                    if PerishSong:
                        PerishCount += 1
                    different_text = False
                    just_sent_out = False
                    pyd.press('z')

                elif move_used.find('Foe') != 0 and ('can’t' in move_used or 'can\'t' in move_used) and 'use' in move_used and continue_text(move_used_img_base, False):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        my_move_first = False
                    else:
                        my_move_first = True
                    if PerishSong:
                        PerishCount += 1
                    different_text = False
                    just_sent_out = False
                    pyd.press('z')

                elif 'potion' in move_used or 'full restore' in move_used or (move_used.find('Foe') == 0 
                and ((('can’t' in move_used or 'can\'t' in move_used) and ' move' in move_used) or ('is fast' in move_used) or 
                (' is' in move_used and ('frozen' in move_used or 'solid' in move_used)) or ('flinched' in move_used) or 
                ('recharge' in move_used) or ('by love' in move_used))):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        opp_move_first = False
                    else:
                        opp_move_first = True
                    different_text = False
                    just_sent_out = False

                elif move_used.find('Foe') == 0 and ('sprang up' in move_used or 'dug a hole' in move_used or (' hid' in move_used 
                and 'underwater' in move_used) or (' flew' in move_used and ' high' in move_used) or (' up ' in move_used and 
                'whirlwind' in move_used) or ('lowered' in move_used and 'head' in move_used) or ('glowing' in move_used) or 
                (' took' in move_used and 'sunlight' in move_used)):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        opp_move_first = False
                    else:
                        opp_move_first = True
                    different_text = False
                    just_sent_out = False
                    
                # len of move used < prev move used length -> different text = true ; break -> different text = true ; after a statement occurs -> different text = false and when loop occurs -> prev length = length of inside text ; just_sent_out -> false when another statement occurs if true when fainted +1 turn counter
                elif move_used.find('Foe') == 0 and 'confused' in move_used:
                    opp_mon_confused = True
                    different_text = False
                    start2 = time.time()
                    elapsed2 = 0
                    if ' is' in move_used:
                        while elapsed2 < 3:
                            # confused_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
                            with mss.mss() as sct:
                                confused_img = sct.grab((1029, 531, 1747, 655))
                            # confused_img = np.array(confused_img)
                            confused_img = edit_image(confused_img)
                            confused = pyt.image_to_string(confused_img, lang='FireRedver1')
                            confused = '\n'.join([line.rstrip() for line in confused.splitlines() if line.strip()])
                            confused = confused.capitalize()

                            if len(confused) < prev_text_length:
                                different_text = True
                            
                            prev_text_length = len(confused)

                            if ' hurt' in confused:
                                which_turn += 1
                                if which_turn % 2 == 0:
                                    opp_move_first = False
                                else:
                                    opp_move_first = True
                                break
                            elif len(confused) >= 7:
                                break
                            elapsed2 = time.time() - start2
                
                elif move_used.find('Foe') == 0 and 'snapped' in move_used and 'out' in move_used:
                    opp_mon_confused = False
                    different_text = False
                    just_sent_out = False

                elif move_used.find('Foe') == 0 and 'used' in move_used and ('!' in move_used or '|' in move_used):
                    if opp_last_move != 'Metronome':
                        which_turn += 1
                    if which_turn % 2 == 0:
                        opp_move_first = False
                    else:
                        opp_move_first = True
                    different_text = False
                    just_sent_out = False
                    move_used = move_used.split('\n')[1]
                    move_used = re.sub('[^a-zA-Z-]', '', move_used)
                    # if move_used == 'prc':
                    #     move_used = 'Dig'
                    move_used = dfl.get_close_matches(move_used, Gens1to3_Moves, cutoff=0.1)[0]
                    
                    start2 = time.time()
                    elapsed2 = 0

                    while elapsed2 < 3:
                        # move_missed_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
                        with mss.mss() as sct:
                            move_missed_img = sct.grab((1029, 531, 1747, 655))
                        # move_missed_img = np.array(move_missed_img)
                        move_missed_img = edit_image(move_missed_img)
                        move_missed = pyt.image_to_string(move_missed_img, lang='FireRedver1')
                        move_missed = '\n'.join([line.rstrip() for line in move_missed.splitlines() if line.strip()])
                        move_missed = move_missed.capitalize()

                        if len(move_missed) < prev_text_length:
                            different_text = True
                        
                        prev_text_length = len(move_missed)

                        if (move_missed.find('Foe') != 0 and (' use' in move_missed or ' is ' in move_missed or ' was ' 
                        in move_missed or ' has ' in move_missed or ' must ' in move_missed or 'flinch' in move_missed)) and \
                        (move_used != 'Disable' or disabled_move != ''):
                            break

                        elif move_missed.find('Foe') != 0 and ('sprang up' in move_missed or 'dug a hole' in move_missed or (' hid' in move_missed 
                        and 'underwater' in move_missed) or (' flew' in move_missed and ' high' in move_missed) or (' up ' in move_missed and 
                        'whirlwind' in move_missed) or ('lowered' in move_missed and 'head' in move_missed) or ('glowing' in move_missed) or 
                        (' took' in move_missed and 'sunlight' in move_missed)):
                            which_turn += 1
                            if which_turn % 2 == 0:
                                my_move_first = False
                            else:
                                my_move_first = True
                            if Taunt:
                                TauntCount += 1
                            if PerishSong:
                                PerishCount += 1
                            different_text = False
                            break

                        elif move_missed.find('Foe') != 0 and 'disabled' in move_missed and 'no more' in move_missed:
                            disabled_move = ''
                            break

                        elif 'reflect' in move_missed and 'wore off' in move_missed:
                            reflect_on = 'false'
                            break

                        elif 'light screen' in move_missed and 'wore off' in move_missed:
                            lightscreen_on = 'false'
                            break

                        elif 'no longer' in move_missed and 'protected' in move_missed:
                            Safeguard = False
                            break

                        elif 'encore' in move_missed and 'ended' in move_missed:
                            Encore = False
                            break
                        
                        elif 'fainted' in move_missed:
                            break

                        elif move_used == 'Taunt' and 'fell for' in move_missed and 'the' in move_missed:
                            Taunt = True
                            TauntCount = 0
                            if opp_move_first == False and TauntCount < 1:
                                TauntCount == 1
                            break

                        elif move_used == 'Perish Song' and 'All ' in move_missed and 'faint' in move_missed and 'turns' in move_missed:
                            PerishSong = True
                            PerishCount = 0
                            if opp_move_first == False and PerishCount < 1:
                                PerishCount = 1
                            break

                        elif move_used == 'Transform' and 'into' in move_missed and ('!' in move_missed or '|' in move_missed):
                            opp_name = move_missed.split()[-1:][0][:-1]
                            opp_mon = dfl.get_close_matches(opp_name, Gen1_Pokemon, cutoff=0.1)[0]
                            for i in opp_move_used:
                                if 'NoAdd' not in i:
                                    i.append('NoAdd')
                            break

                        elif move_used == 'Disable' and 'disabled' in move_missed:
                            move_disabled = move_missed.split('\n')[0]
                            move_disabled = ' '.join(move_disabled.split()[1:])
                            move_disabled = dfl.get_close_matches(move_disabled, Gens1to3_Moves, cutoff=0.1)[0]
                            # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
                            disabled_move = move_disabled
                            break

                        elif 'missed' in move_missed or 'evaded' in move_missed or 'prevents' in move_missed or \
                        'failed' in move_missed or 'blocks' in move_missed or (('doesn’t' in move_missed or 'doesn\'t' 
                        in move_missed) and 'affect') or (' no ' in move_missed and 'target' in move_missed) or \
                        (move_missed.find('Foe') != 0 and 'protected' in move_missed):
                            already_add = True
                            opp_move_used.append([move_used, False])
                            if move_used not in actual_moves and opp_last_move != 'Metronome':
                                move_added = True
                                actual_moves.append(move_used)
                            break
                        
                        elif 'fell!' in move_missed or 'rose!' in move_missed or 'fell !' in move_missed or 'rose !' in move_missed:
                            already_add = True
                            opp_move_used.append([move_used, True, True])
                            if move_used not in actual_moves and opp_last_move != 'Metronome':
                                move_added = True
                                actual_moves.append(move_used)
                            break

                        elapsed2 = time.time() - start2
                
                    if already_add == False:
                        opp_move_used.append([move_used, True])

                        if move_used not in actual_moves and opp_last_move != 'Metronome':
                            move_added = True
                            actual_moves.append(move_used)

                    opp_last_move = move_used

                elif move_used.find('Foe') == 0 and 'is disabled' in move_used and continue_text(move_used_img_base, False):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        opp_move_first = False
                    else:
                        opp_move_first = True
                    different_text = False
                    just_sent_out = False
                    pyd.press('z')

                elif move_used.find('Foe') == 0 and ('can’t' in move_used or 'can\'t' in move_used) and 'use' in move_used and continue_text(move_used_img_base, False):
                    which_turn += 1
                    if which_turn % 2 == 0:
                        opp_move_first = False
                    else:
                        opp_move_first = True
                    different_text = False
                    just_sent_out = False
                    pyd.press('z')

                elif move_used.find('Foe') != 0 and 'disabled' in move_used and 'no more' in move_used:
                    disabled_move = ''
                    different_text = False
        
                elif 'reflect' in move_used and 'wore off' in move_used:
                    reflect_on = 'false'
                    different_text = False

                elif 'light screen' in move_used and 'wore off' in move_used:
                    lightscreen_on = 'false'
                    different_text = False
                
                elif 'no longer' in move_used and 'protected' in move_used:
                    Safeguard = False
                    different_text = False

                elif 'encore' in move_used and 'ended' in move_used:
                    Encore = False

                elif 'fainted' in move_used and continue_text(move_used_img_base, False):
                    # print('fainted')
                    different_text = False
                    if move_used.find('Foe') == 0:
                        which_turn = 0
                        prev_opp_faint = True
                        opp_mon_faint = True
                        no_stat_change = False
                        no_new_moves = False
                        KeepSeed = False
                        KeepMon = False
                        for i in opp_move_used:
                            if 'NoAdd' not in i:
                                i.append('NoAdd')
                        if just_sent_out:
                            if Taunt:
                                TauntCount += 1
                            if PerishSong:
                                PerishCount += 1
                    elif move_used.find('Foe') != 0:
                        my_mon_faint = True
                    pyd.press('z')

                    while tutorial:
                        pyd.press('z')
                        if get_color(1445, 357) == (0, 0, 0):
                            exit()

                elif 'withdrew' in move_used and 'used' not in move_used:
                    opp_made_switch = True
                    different_text = False

                elif 'sent' in move_used and 'out' in move_used:
                    just_sent_out = True
                    opp_switch = True
                    if my_actual_move in ('Hyper Beam', 'Frenzy Plant', 'Blast Burn', 'Hydro Cannon', 'Outrage', 'Petal Dance') and my_move_used == True and prev_opp_faint == True:
                        no_stat_change = True
                        no_new_moves = True
                        opp_stat_stages = [0, 0, 0, 0, 0]
                        actual_moves = []
                        move_added = False
                    elif prev_opp_faint == False:
                        if len(opp_move_used) > 0 and opp_move_used[len(opp_move_used)-1][0] == 'Baton Pass' and opp_move_used[len(opp_move_used)-1][1] == True:
                            actual_moves = []
                            move_added = False
                            just_sent_out = False
                    if opp_made_switch:
                        no_stat_change = True
                        no_new_moves = True
                        opp_stat_stages = [0, 0, 0, 0, 0]
                        actual_moves = []
                        move_added = False
                        just_sent_out = False
                    prev_opp_faint = False
                    opp_made_switch = False
                    different_text = False
                
                elif 'make' in move_used and 'room' in move_used:
                    time.sleep(1.5)
                    pyd.press('z')
                    time.sleep(2.5)
                    learn_move()
                    time.sleep(2.5)
                    if continue_text(move_used_img_base, False) == False:
                        pyd.press('z')
                
                elif ('out of' in move_used and 'usable' in move_used) or ('Player' in move_used and 'defeated' in move_used):
                    while get_color(1043, 515) == (200, 168, 72) and get_color(1043, 533) == (40, 80, 104):
                        pyd.press('z')
                    exit()

                elif continue_text(move_used_img_base, False):
                    different_text = True
                    pyd.press('z')

                elif lvl_box == (208, 160, 208):
                    different_text = True
                    pyd.press('z')
                
            elapsed = time.time() - start
        
        # print('Actual moves:')
        # print(actual_moves)
        # print('Opp used:')
        # print(opp_move_used)

        while tutorial and get_color(1026, 579) == (160, 208, 224) and get_color(1873, 579) == (160, 208, 224):
            with mss.mss() as sct:
                battle_start_img_base = np.array(sct.grab((1010, 510, 1890, 670)))
            if continue_text(battle_start_img_base, False):
                pyd.press('z')

        if len(opp_move_used) > 0 and opp_move_used[0][0] == 'Haze' and opp_move_used[0][1] == True:
            my_stat_stages = [0, 0, 0, 0, 0]
            opp_stat_stages = [0, 0, 0, 0, 0]
        
        if my_actual_move == 'Haze' and my_move_used == True:
            my_stat_stages = [0, 0, 0, 0, 0]
            opp_stat_stages = [0, 0, 0, 0, 0]
        
        if TauntCount >= 2:
            Taunt = False

        if my_actual_move == 'Brick Break' and my_move_used == True:
            reflect_on = 'false'
            lightscreen_on = 'false'

        if my_actual_move == 'Leed Seed' and my_move_used == True:
            LeechSeed = True

        if len(opp_move_used) > 0 and opp_move_used[0][0] == 'Transform' and opp_move_used[0][1] == True and opp_move_first == True and 'NoAdd' not in opp_move_used[0]:
            opp_stat_stages = my_stat_stages
            no_stat_change = True
            KeepMon = True

# moves that the opp used that affect its stat go in the bottom
        if my_move_used == True and my_stat_changed == True:
            if my_actual_move in ('Metal Claw', 'Meteor Mash'):
                my_stat_stages[0] += 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif my_actual_move == 'Aurora Beam':
                opp_stat_stages[0] -= 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6)-6)

            elif my_actual_move == 'Steel Wing':
                my_stat_stages[1] += 1
                my_stat_stages[1] = max(min(my_stat_stages[1], 6)-6)
            
            elif my_actual_move in ('Acid', 'Crush Claw', 'Iron Tail', 'Rock Smash'):
                opp_stat_stages[1] -= 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
            
            elif my_actual_move == 'Mist Ball':
                opp_stat_stages[2] -= 1
                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6)-6)

            elif my_actual_move in ('Crunch', 'Luster Purge', 'Psychic', 'Shadow Ball'):
                opp_stat_stages[3] -= 1
                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6)-6)

            elif my_actual_move in ('Bubble', 'BubbleBeam', 'Constrict'):
                opp_stat_stages[4] -= 1
                opp_stat_stages[4] = max(min(opp_stat_stages[4], 6)-6)

            elif my_actual_move in ('Ancient Power', 'Silver Wind'):
                my_stat_stages[0] += 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)
                my_stat_stages[1] += 1
                my_stat_stages[1] = max(min(my_stat_stages[1], 6)-6)
                my_stat_stages[2] += 1
                my_stat_stages[2] = max(min(my_stat_stages[2], 6)-6)
                my_stat_stages[3] += 1
                my_stat_stages[3] = max(min(my_stat_stages[3], 6)-6)
                my_stat_stages[4] += 1
                my_stat_stages[4] = max(min(my_stat_stages[4], 6)-6)

        if my_actual_move in status_moves and my_move_used == True:
            if len(status_moves[usable_status_moves[0][1]]) == 3:
                if status_moves[usable_status_moves[0][1]][2] == 'target':
                    if status_moves[usable_status_moves[0][1]][1] == 'atk':
                        opp_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'def':
                        opp_stat_stages[1] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spa':
                        opp_stat_stages[2] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spd':
                        opp_stat_stages[3] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spe':
                        opp_stat_stages[4] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
                else:
                    if status_moves[usable_status_moves[0][1]][1] == 'atk':
                        my_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'def':
                        my_stat_stages[1] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spa':
                        my_stat_stages[2] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spd':
                        my_stat_stages[3] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spe':
                        my_stat_stages[4] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
            elif len(status_moves[usable_status_moves[0][1]]) == 5:
                if status_moves[usable_status_moves[0][1]][4] == 'target':
                    if status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'def':
                        opp_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[usable_status_moves[0][1]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'spe':
                        opp_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[4] += status_moves[usable_status_moves[0][1]][2]
                        opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'spa':
                        opp_stat_stages[0] += status_moves[opp_move_used[1]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[2], 6), -6)
                        opp_stat_stages[2] += status_moves[opp_move_used[1]][2]
                        opp_stat_stages[2] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spa' and status_moves[usable_status_moves[0][1]][3] == 'spd':
                        opp_stat_stages[2] += status_moves[opp_move_used[1]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                        opp_stat_stages[3] += status_moves[opp_move_used[1]][2]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                else:
                    if status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'def':
                        my_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[1] += status_moves[usable_status_moves[0][1]][2]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'spe':
                        my_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[4] += status_moves[usable_status_moves[0][1]][2]
                        my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'spa' and status_moves[usable_status_moves[0][1]][3] == 'spd':
                        my_stat_stages[2] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                        my_stat_stages[3] += status_moves[usable_status_moves[0][1]][2]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
            else:
                if status_moves[usable_status_moves[0][1]][6] == 'user':
                    if status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'def' and status_moves[usable_status_moves[0][1]][5] == 'spe':
                        my_stat_stages[0] += status_moves[usable_status_moves[0][1]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[1] += status_moves[usable_status_moves[0][1]][2]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                        my_stat_stages[4] += status_moves[usable_status_moves[0][1]][4]
                        my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
        elif my_actual_move in status_moves:
            check_status_move = False

        if opp_mon_faint == False:
            if opp_switch == True or (my_actual_move in ('Whirlwind', 'Roar') and my_move_used == True):
                new_opp_mon = True
                no_switch = False

        else:
            # check if battle is done
            new_opp_mon = True
            no_switch = False

                # if mon faint and faint count is different add
                # already out and reset stat changes
                # hybeam faint sd add: < 1 or used after opp faint (everything above (in the other section) is before opp faint), sd hybeam faint dont add
                # change prev list length to boolean
                # add foe intimidate cut attack to this section and above section
                # used before faint check if faint count is the same (dont add) then its before if faint count is different (add) than its after
                # disable wears off exactly after opp mon faints and after pressing A and before sending out new mon
                # whenever opp mon faints you have to press a immediately after (before the next action begins)
            # opp mon faints after switching in my mon
        # transform go first or second before or after whirlwind
        
        forced_switch = False
        forced_switch2 = False

        if len(opp_move_used) > 0:
            if opp_move_used[0][0] in ('Whirlwind', 'Roar') and opp_move_used[0][1] == True:
                switch_mon = True
                my_mon_struggle = False
        
        if len(opp_move_used) > 1:
            if opp_move_used[1][0] in ('Whirlwind', 'Roar') and opp_move_used[1][1] == True:
                forced_switch = True
                my_mon_struggle = False
        
        if len(opp_move_used) > 2:
            if opp_move_used[2][0] in ('Whirlwind', 'Roar') and opp_move_used[2][1] == True:
                forced_switch2 = True
                my_mon_struggle = False
        
        if switch_mon == True:
            # print('getting new mon')
            my_mon = get_pokemon_name('plyr')
            my_mon_lvl = get_pokemon_level('plyr')
            my_stat_stages = [0, 0, 0, 0, 0]
            my_accuracy = 0
            check_status_move = False
            prev_move = 0
            disabled_move = ''
            make_switch = False
            my_mon_faint = False
            PerishSong = False
            PerishCount = 0
            Taunt = False
            TauntCount = 0
            Torment = False
            my_mon_confused = False
            new_my_mon = False
            Encore = False
            # print(my_mon_lvl)
            # if forced switch + opp move not transform

        if len(opp_move_used) > 0 and opp_move_used[0][0] == 'Transform' and opp_move_used[0][1] == True and opp_move_first == False and 'NoAdd' not in opp_move_used[0]:
            opp_stat_stages = my_stat_stages
            no_stat_change = True
            KeepMon = True

        if forced_switch == False and len(opp_move_used) > 0 and opp_move_used[0][0] in status_moves and opp_move_used[0][1] == True:
            if len(status_moves[opp_move_used[0][0]]) == 3:
                if status_moves[opp_move_used[0][0]][2] == 'target':
                    if status_moves[opp_move_used[0][0]][1] == 'atk':
                        my_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'def':
                        my_stat_stages[1] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spa':
                        my_stat_stages[2] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spd':
                        my_stat_stages[3] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spe':
                        my_stat_stages[4] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
            else:
                if status_moves[opp_move_used[0][0]][4] == 'target':
                    if status_moves[opp_move_used[0][0]][1] == 'atk' and status_moves[opp_move_used[0][0]][3] == 'def':
                        my_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[1] += status_moves[opp_move_used[0][0]][2]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'atk' and status_moves[opp_move_used[0][0]][3] == 'spe':
                        my_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[4] += status_moves[opp_move_used[0][0]][2]
                        my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[usable_status_moves[0][1]][1] == 'atk' and status_moves[usable_status_moves[0][1]][3] == 'spa':
                        my_stat_stages[0] += status_moves[opp_move_used[1]][0]
                        my_stat_stages[0] = max(min(opp_stat_stages[2], 6), -6)
                        my_stat_stages[2] += status_moves[opp_move_used[1]][2]
                        my_stat_stages[2] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spa' and status_moves[opp_move_used[0][0]][3] == 'spd':
                        my_stat_stages[2] += status_moves[opp_move_used[0][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                        my_stat_stages[3] += status_moves[opp_move_used[0][0]][2]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)

        if forced_switch == False and len(opp_move_used) > 0 and len(opp_move_used[0]) >= 3 and opp_move_used[0][2] == True:
            if opp_move_used[0][0] == 'Aurora Beam':
                my_stat_stages[0] -= 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[0][0] in ('Acid', 'Crush Claw', 'Iron Tail', 'Rock Smash'):
                my_stat_stages[1] -= 1
                my_stat_stages[1] = max(min(my_stat_stages[1], 6)-6)
            
            elif opp_move_used[0][0] == 'Mist Ball':
                my_stat_stages[2] -= 1
                my_stat_stages[2] = max(min(my_stat_stages[2], 6)-6)

            elif opp_move_used[0][0] in ('Crunch', 'Luster Purge', 'Psychic', 'Shadow Ball'):
                my_stat_stages[3] -= 1
                my_stat_stages[3] = max(min(my_stat_stages[3], 6)-6)

            elif opp_move_used[0][0] in ('Bubble', 'BubbleBeam', 'Constrict'):
                my_stat_stages[4] -= 1
                my_stat_stages[4] = max(min(my_stat_stages[4], 6)-6)

            elif opp_move_used[0][0] in ('Muddy Water', 'Octozooka'):
                my_accuracy -= 1
                my_accuracy = max(min(my_accuracy, 6), -6)

        if len(opp_move_used) > 1 and opp_move_used[1][0] == 'Transform' and opp_move_used[1][1] == True and 'NoAdd' not in opp_move_used[1]:
            opp_stat_stages = my_stat_stages
            no_stat_change = True
            KeepMon = True

        if forced_switch:
            my_stat_stages = [0, 0, 0, 0, 0]
            no_my_stat_change = True
            new_my_mon = True
            switch_mon = False

        if forced_switch2 == False and len(opp_move_used) > 1 and opp_move_used[1][0] in status_moves and opp_move_used[1][1] == True:
            if len(status_moves[opp_move_used[1][0]]) == 3:
                if status_moves[opp_move_used[1][0]][2] == 'target':
                    if status_moves[opp_move_used[1][0]][1] == 'atk':
                        my_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'def':
                        my_stat_stages[1] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spa':
                        my_stat_stages[2] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spd':
                        my_stat_stages[3] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spe':
                        my_stat_stages[4] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
            else:
                if status_moves[opp_move_used[1][0]][4] == 'target':
                    if status_moves[opp_move_used[1][0]][1] == 'atk' and status_moves[opp_move_used[1][0]][3] == 'def':
                        my_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[1] += status_moves[opp_move_used[1][0]][2]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'atk' and status_moves[opp_move_used[1][0]][3] == 'spe':
                        my_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[4] += status_moves[opp_move_used[1][0]][2]
                        my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spa' and status_moves[opp_move_used[1][0]][3] == 'spd':
                        my_stat_stages[2] += status_moves[opp_move_used[1][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                        my_stat_stages[3] += status_moves[opp_move_used[1][0]][2]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
        
        if forced_switch2 == False and len(opp_move_used) > 1 and len(opp_move_used[1]) > 2 and opp_move_used[1][2] == True:
            if opp_move_used[1][0] == 'Aurora Beam':
                my_stat_stages[0] -= 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[1][0] in ('Acid', 'Crush Claw', 'Iron Tail', 'Rock Smash'):
                my_stat_stages[1] -= 1
                my_stat_stages[1] = max(min(my_stat_stages[1], 6)-6)
            
            elif opp_move_used[1][0] == 'Mist Ball':
                my_stat_stages[2] -= 1
                my_stat_stages[2] = max(min(my_stat_stages[2], 6)-6)

            elif opp_move_used[1][0] in ('Crunch', 'Luster Purge', 'Psychic', 'Shadow Ball'):
                my_stat_stages[3] -= 1
                my_stat_stages[3] = max(min(my_stat_stages[3], 6)-6)

            elif opp_move_used[1][0] in ('Bubble', 'BubbleBeam', 'Constrict'):
                my_stat_stages[4] -= 1
                my_stat_stages[4] = max(min(my_stat_stages[4], 6)-6)

            elif opp_move_used[1][0] in ('Muddy Water', 'Octozooka'):
                my_accuracy -= 1
                my_accuracy = max(min(my_accuracy, 6), -6)

        if len(opp_move_used) > 2 and opp_move_used[2][0] in status_moves and opp_move_used[2][1] == True:
            if len(status_moves[opp_move_used[2][0]]) == 3:
                if status_moves[opp_move_used[2][0]][2] == 'target':
                    if status_moves[opp_move_used[2][0]][1] == 'atk':
                        my_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'def':
                        my_stat_stages[1] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spa':
                        my_stat_stages[2] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spd':
                        my_stat_stages[3] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spe':
                        my_stat_stages[4] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
            else:
                if status_moves[opp_move_used[2][0]][4] == 'target':
                    if status_moves[opp_move_used[2][0]][1] == 'atk' and status_moves[opp_move_used[2][0]][3] == 'def':
                        my_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[1] += status_moves[opp_move_used[2][0]][2]
                        my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'atk' and status_moves[opp_move_used[2][0]][3] == 'spe':
                        my_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        my_stat_stages[4] += status_moves[opp_move_used[2][0]][2]
                        my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spa' and status_moves[opp_move_used[2][0]][3] == 'spd':
                        my_stat_stages[2] += status_moves[opp_move_used[2][0]][0]
                        my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                        my_stat_stages[3] += status_moves[opp_move_used[2][0]][2]
                        my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
        
        if len(opp_move_used) > 2 and len(opp_move_used[2]) > 2 and opp_move_used[1][2] == True:
            if opp_move_used[1][0] == 'Aurora Beam':
                my_stat_stages[0] -= 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[1][0] in ('Acid', 'Crush Claw', 'Iron Tail', 'Rock Smash'):
                my_stat_stages[1] -= 1
                my_stat_stages[1] = max(min(my_stat_stages[1], 6)-6)
            
            elif opp_move_used[1][0] == 'Mist Ball':
                my_stat_stages[2] -= 1
                my_stat_stages[2] = max(min(my_stat_stages[2], 6)-6)

            elif opp_move_used[1][0] in ('Crunch', 'Luster Purge', 'Psychic', 'Shadow Ball'):
                my_stat_stages[3] -= 1
                my_stat_stages[3] = max(min(my_stat_stages[3], 6)-6)

            elif opp_move_used[1][0] in ('Bubble', 'BubbleBeam', 'Constrict'):
                my_stat_stages[4] -= 1
                my_stat_stages[4] = max(min(my_stat_stages[4], 6)-6)

            elif opp_move_used[1][0] in ('Muddy Water', 'Octozooka'):
                my_accuracy -= 1
                my_accuracy = max(min(my_accuracy, 6), -6)
            
        if len(opp_move_used) > 2 and opp_move_used[2][0] == 'Transform' and opp_move_used[2][1] == True and 'NoAdd' not in opp_move_used[2]:
            opp_stat_stages = my_stat_stages
            no_stat_change = True
            KeepMon = True

        if forced_switch2:
            my_stat_stages = [0, 0, 0, 0, 0]
            no_my_stat_change = True
            new_my_mon = True
            switch_mon = False
        
        if forced_switch == False and len(opp_move_used) > 0 and opp_move_used[0][0] in ('Flash', 'Kinesis', 'Mud-Slap', 'Sand-Attack', 'SmokeScreen') and opp_move_used[0][1] == True:
            my_accuracy -= 1
            my_accuracy = max(min(my_accuracy, 6)-6)

        if forced_switch2 == False and len(opp_move_used) > 1 and opp_move_used[1][0] in ('Flash', 'Kinesis', 'Mud-Slap', 'Sand-Attack', 'SmokeScreen') and opp_move_used[1][1] == True:
            my_accuracy -= 1
            my_accuracy = max(min(my_accuracy, 6)-6)

        if len(opp_move_used) > 2 and opp_move_used[2][0] in ('Flash', 'Kinesis', 'Mud-Slap', 'Sand-Attack', 'SmokeScreen') and opp_move_used[2][1] == True:
            my_accuracy -= 1
            my_accuracy = max(min(my_accuracy, 6)-6)

                # switch in
                # disable fails b/c switch mon = True -> new mon = True
                # disable moves first
                # disable fails b/c less than 2 seconds and new mon = True
                # my mon attacks second (used move = True -> new mon = False)
                # disable first
                # disable hits (works when new_my_mon == False)
            
        if my_mon_faint == False:
            if my_mon_struggle == True and opp_mon_faint == False and (opp_mon not in ('Diglett', 'Dugtrio') or 
            'Flying' in get_mon_type(my_mon) or my_mon in ('Gastly', 'Haunter', 'Gengar')):
                make_switch = True
            else:
                make_switch = False

        else:
            new_my_mon = True
            make_switch = True
            switch_mon = False
            no_switch = False
            my_mon_struggle = False

            # check for opp faint
            # change the border to be top left
            # add other effect moves here
        
        if len(opp_move_used) > 0:
            if opp_move_first == False and opp_move_used[0][0] == 'Haze' and opp_move_used[0][1] == True:
                my_stat_stages = [0, 0, 0, 0, 0]
        
        if len(opp_move_used) > 0 and opp_move_used[0][0] in status_moves and opp_move_used[0][1] == True and 'NoAdd' not in opp_move_used[0]:
            if len(status_moves[opp_move_used[0][0]]) == 3:
                if status_moves[opp_move_used[0][0]][2] == 'user':
                    if status_moves[opp_move_used[0][0]][1] == 'atk':
                        opp_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'def':
                        opp_stat_stages[1] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spa':
                        opp_stat_stages[2] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spd':
                        opp_stat_stages[3] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spe':
                        opp_stat_stages[4] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
            elif len(status_moves[opp_move_used[1][0]]) == 5:
                if status_moves[opp_move_used[0][0]][4] == 'user':
                    if status_moves[opp_move_used[0][0]][1] == 'atk' and status_moves[opp_move_used[0][0]][3] == 'def':
                        opp_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[0][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'atk' and status_moves[opp_move_used[0][0]][3] == 'spe':
                        opp_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[0][0]][2]
                        opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[0][0]][1] == 'spa' and status_moves[opp_move_used[0][0]][3] == 'spd':
                        opp_stat_stages[2] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                        opp_stat_stages[3] += status_moves[opp_move_used[0][0]][2]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
            else:
                if status_moves[opp_move_used[0][0]][6] == 'user':
                    if status_moves[opp_move_used[0][0]][1] == 'atk' and status_moves[opp_move_used[0][0]][3] == 'def' \
                    and status_moves[opp_move_used[0][0]][5] == 'spe' and (opp_move_used[0][0] != 'Curse' or 'Ghost' not in get_mon_type(opp_mon)):
                        opp_stat_stages[0] += status_moves[opp_move_used[0][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[0][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[0][0]][4]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
        
        elif len(opp_move_used) > 0 and len(opp_move_used[0]) > 2 and opp_move_used[0][2] == True and 'NoAdd' not in opp_move_used[0]:
            if opp_move_used[0][0] in ('Metal Claw', 'Meteor Mash'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[0][0] == 'Steel Wing':
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
            
            elif opp_move_used[0][0] in ('Ancient Power', 'Silver Wind'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6)-6)
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
                opp_stat_stages[2] += 1
                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6)-6)
                opp_stat_stages[3] += 1
                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6)-6)
                opp_stat_stages[4] += 1
                opp_stat_stages[4] = max(min(opp_stat_stages[4], 6)-6)

        if len(opp_move_used) > 1:
            if opp_move_used[1][0] == 'Haze' and opp_move_used[1][1] == True:
                my_stat_stages = [0, 0, 0, 0, 0]
                opp_stat_stages = [0, 0, 0, 0, 0]
        
        if my_move_first == False and my_actual_move == 'Haze' and my_move_used == True:
            opp_stat_stages = [0, 0, 0, 0, 0]

        if len(opp_move_used) > 1 and opp_move_used[1][0] in status_moves and opp_move_used[1][1] == True and 'NoAdd' not in opp_move_used[1]:
            if len(status_moves[opp_move_used[1][0]]) == 3:
                if status_moves[opp_move_used[1][0]][2] == 'user':
                    if status_moves[opp_move_used[1][0]][1] == 'atk':
                        opp_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'def':
                        opp_stat_stages[1] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spa':
                        opp_stat_stages[2] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spd':
                        opp_stat_stages[3] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spe':
                        opp_stat_stages[4] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
            elif len(status_moves[opp_move_used[1][0]]) == 5:
                if status_moves[opp_move_used[1][0]][4] == 'user':
                    if status_moves[opp_move_used[1][0]][1] == 'atk' and status_moves[opp_move_used[1][0]][3] == 'def':
                        opp_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[1][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'atk' and status_moves[opp_move_used[1][0]][3] == 'spe':
                        opp_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[1][0]][2]
                        opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[1][0]][1] == 'spa' and status_moves[opp_move_used[1][0]][3] == 'spd':
                        opp_stat_stages[2] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                        opp_stat_stages[3] += status_moves[opp_move_used[1][0]][2]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
            else:
                if status_moves[opp_move_used[1][0]][6] == 'user':
                    if status_moves[opp_move_used[1][0]][1] == 'atk' and status_moves[opp_move_used[1][0]][3] == 'def' \
                    and status_moves[opp_move_used[1][0]][5] == 'spe' and (opp_move_used[1][0] != 'Curse' or 'Ghost' not in get_mon_type(opp_mon)):
                        opp_stat_stages[0] += status_moves[opp_move_used[1][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[1][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[1][0]][4]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
        
        elif len(opp_move_used) > 1 and len(opp_move_used[1]) == 3 and opp_move_used[1][2] == True and 'NoAdd' not in opp_move_used[1]:
            if opp_move_used[1][0] in ('Metal Claw', 'Meteor Mash'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[1][0] == 'Steel Wing':
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
            
            elif opp_move_used[1][0] in ('Ancient Power', 'Silver Wind'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6)-6)
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
                opp_stat_stages[2] += 1
                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6)-6)
                opp_stat_stages[3] += 1
                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6)-6)
                opp_stat_stages[4] += 1
                opp_stat_stages[4] = max(min(opp_stat_stages[4], 6)-6)
        
        if len(opp_move_used) > 2:
            if opp_move_used[2] != None and opp_move_used[2][0] == 'Haze' and opp_move_used[2][1] == True:
                my_stat_stages = [0, 0, 0, 0, 0]
                opp_stat_stages = [0, 0, 0, 0, 0]

        if len(opp_move_used) > 2 and opp_move_used[2][0] in status_moves and opp_move_used[2][1] == True and 'NoAdd' not in opp_move_used[2]:
            if len(status_moves[opp_move_used[2][0]]) == 3:
                if status_moves[opp_move_used[2][0]][2] == 'user':
                    if status_moves[opp_move_used[2][0]][1] == 'atk':
                        opp_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'def':
                        opp_stat_stages[1] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spa':
                        opp_stat_stages[2] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spd':
                        opp_stat_stages[3] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spe':
                        opp_stat_stages[4] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
            elif len(status_moves[opp_move_used[2][0]]) == 5:
                if status_moves[opp_move_used[2][0]][4] == 'user':
                    if status_moves[opp_move_used[2][0]][1] == 'atk' and status_moves[opp_move_used[2][0]][3] == 'def':
                        opp_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[2][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'atk' and status_moves[opp_move_used[2][0]][3] == 'spe':
                        opp_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[2][0]][2]
                        opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                    elif status_moves[opp_move_used[2][0]][1] == 'spa' and status_moves[opp_move_used[2][0]][3] == 'spd':
                        opp_stat_stages[2] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                        opp_stat_stages[3] += status_moves[opp_move_used[2][0]][2]
                        opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
            else:
                if status_moves[opp_move_used[2][0]][6] == 'user':
                    if status_moves[opp_move_used[2][0]][1] == 'atk' and status_moves[opp_move_used[2][0]][3] == 'def' \
                    and status_moves[opp_move_used[2][0]][5] == 'spe' and (opp_move_used[2][0] != 'Curse' or 'Ghost' not in get_mon_type(opp_mon)):
                        opp_stat_stages[0] += status_moves[opp_move_used[2][0]][0]
                        opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        opp_stat_stages[1] += status_moves[opp_move_used[2][0]][2]
                        opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                        opp_stat_stages[4] += status_moves[opp_move_used[2][0]][4]
                        opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
        
        elif len(opp_move_used) > 2 and len(opp_move_used[2]) == 3 and opp_move_used[2][2] == True and 'NoAdd' not in opp_move_used[2]:
            if opp_move_used[2][0] in ('Metal Claw', 'Meteor Mash'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(my_stat_stages[0], 6)-6)

            elif opp_move_used[2][0] == 'Steel Wing':
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
            
            elif opp_move_used[2][0] in ('Ancient Power', 'Silver Wind'):
                opp_stat_stages[0] += 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6)-6)
                opp_stat_stages[1] += 1
                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6)-6)
                opp_stat_stages[2] += 1
                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6)-6)
                opp_stat_stages[3] += 1
                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6)-6)
                opp_stat_stages[4] += 1
                opp_stat_stages[4] = max(min(opp_stat_stages[4], 6)-6)

        if my_mon_faint == False:
            if len(opp_move_used) > 0:
                if forced_switch == False and opp_move_used[0][0] == 'Encore' and opp_move_used[0][1] == True:
                    Encore = True
            if len(opp_move_used) > 1:
                if forced_switch2 == False and opp_move_used[1][0] == 'Encore' and opp_move_used[1][1] == True:
                    Encore = True
            if len(opp_move_used) > 2:
                if opp_move_used[2][0] == 'Encore' and opp_move_used[2][1] == True:
                    Encore = True

            if len(opp_move_used) > 0:
                if forced_switch == False and opp_move_used[0][0] == 'Torment' and opp_move_used[0][1] == True:
                    Torment = True
            if len(opp_move_used) > 1:
                if forced_switch2 == False and opp_move_used[1][0] == 'Torment' and opp_move_used[1][1] == True:
                    Torment = True
            if len(opp_move_used) > 2:
                if opp_move_used[2][0] == 'Torment' and opp_move_used[2][1] == True:
                    Torment = True

            if len(opp_move_used) > 0:
                if forced_switch == False and opp_move_used[0][0] in ('Block', 'Mean Look', 'Bind', 'Clamp', 'Fire Spin', 'Sand Tomb', 'Whirlpool', 'Wrap') and opp_move_used[0][1] == True and 'NoAdd' not in opp_move_used[0]:
                    no_switch = True
                    make_switch = False
                    # print('no switch')
            if len(opp_move_used) > 1:
                if forced_switch2 == False and opp_move_used[1][0] in ('Block', 'Mean Look', 'Bind', 'Clamp', 'Fire Spin', 'Sand Tomb', 'Whirlpool', 'Wrap') and opp_move_used[1][1] == True and 'NoAdd' not in opp_move_used[1]:
                    no_switch = True
                    make_switch = False
            if len(opp_move_used) > 2:
                if opp_move_used[2][0] in ('Block', 'Mean Look', 'Bind', 'Clamp', 'Fire Spin', 'Sand Tomb', 'Whirlpool', 'Wrap') and opp_move_used[2][1] == True and 'NoAdd' not in opp_move_used[2]:
                    no_switch = True
                    make_switch = False
        
        if len(opp_move_used) > 0:
            if (my_actual_move != 'Brick Break' or my_move_used == False or my_move_first == True) and opp_move_used[0][0] == 'Reflect' and opp_move_used[0][1] == True:
                reflect_on = 'true'
            elif (my_actual_move != 'Brick Break' or my_move_used == False or my_move_first == True) and opp_move_used[0][0] == 'Light Screen' and opp_move_used[0][1] == True:
                lightscreen_on = 'true'
        if len(opp_move_used) > 1:
            if opp_move_used[1][0] == 'Reflect' and opp_move_used[1][1] == True:
                reflect_on = 'true'
            elif opp_move_used[1][0] == 'Light Screen' and opp_move_used[1][1] == True:
                lightscreen_on = 'true'
        if len(opp_move_used) > 2:
            if opp_move_used[2][0] == 'Reflect' and opp_move_used[2][1] == True:
                reflect_on = 'true'
            elif opp_move_used[2][0] == 'Light Screen' and opp_move_used[2][1] == True:
                lightscreen_on = 'true'
        
        if len(opp_move_used) > 0:
            if opp_move_used[0][0] == 'Safeguard' and opp_move_used[0][1] == True:
                Safeguard = True
        if len(opp_move_used) > 1:
            if opp_move_used[1][0] == 'Safeguard' and opp_move_used[1][1] == True:
                Safeguard = True
        if len(opp_move_used) > 2:
            if opp_move_used[2][0] == 'Safeguard' and opp_move_used[2][1] == True:
                Safeguard = True

        if len(opp_move_used) > 0:
            if opp_move_used[0][0] == 'Baton Pass' and opp_move_used[0][1] == True and \
            'NoAdd' not in opp_move_used[0] and (my_actual_move not in ('Whirlwind', 'Roar') or my_move_used == False):
                new_opp_mon = True
                no_switch = False
                no_stat_change = True
                no_new_moves = True
                KeepSeed = True
        if len(opp_move_used) > 1:
            if opp_move_used[1][0] == 'Baton Pass' and opp_move_used[1][1] == True and 'NoAdd' not in opp_move_used[1]:
                new_opp_mon = True
                no_switch = False
                no_stat_change = True
                no_new_moves = True
                KeepSeed = True
        if len(opp_move_used) > 2:
            if opp_move_used[2][0] == 'Baton Pass' and opp_move_used[2][1] == True and 'NoAdd' not in opp_move_used[2]:
                new_opp_mon = True
                no_switch = False
                no_stat_change = True
                no_new_moves = True
                KeepSeed = True

        # reset when haze goes after a status move or when haze is the second move or if switch_mon = true or if my move first = false
        # print('my stat stages:')
        # print(my_stat_stages)
        
        forced_switch = False
        forced_switch2 = False
        make_move = False
    
    # must recharge
    # can't use after the taunt
    # taunt (2 turns, +1 on the turn used), torment (until switch out), turn counter (+1 everytime opp attacks or switches in when not fainting, opp faints +1)
    # sending in pokemon variable like start of battle to prevent checking for new pokemon and waiting for 8 seconds 
    # and variable turns off after battle phase is done
    # switch_mon variable to make new_my_mon true
    # wait 3 seconds after switching in new pokemon
    # separate moveset for moves the opposing pokemon actually used
    # fix switch in and use disable, then use disable first next turn
    # fix last usable move is disabled
    # use a setup move based on HP of my pokemon and opposing pokemon (maybe)
        # if opposing pokemon does less than or equal to 25% HP and my pokemon is above 75% HP use a setup move once
        # or if a pokemon is same level use a setup move once
    # struggle -> switch if my mon hasn't fainted and opp hasn't fainted, check new opp before switching if struggle kos opp
    # prioritize learning moves that are STAB, higher base power, and higher accuracy
        # learn moves that are stab or synergize with the highest attacking stat, have at least 85% accuracy, higher base power, coverage
        # get rid of lowest accuracy move (< 85) then lowest base power move
        # keep stat boosting moves that raise power of STAB moves or moves that match highest attacking stat, hm moves
    # check timing of switch (1.1 seconds)
    # 2 turn moves like solar beam
    # asleep and paralyzed check for status moves
    # make sure to not add stat change for my mon sent in and opp mon already out after my mon koed
    # move stat change for my mon to mid battle part (last part) and don't add if my mon koed
    # prevent from checking moves after my mon faint