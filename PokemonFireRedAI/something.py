import os
import time
import re
import math
import cv2
import subprocess
import imageio
import numpy as np
import pandas as pd
import difflib as dfl
import pypokedex as pyp
import pytesseract as pyt
import pydirectinput as pyd
from PIL import Image, ImageGrab, ImageChops, ImageOps, ImageDraw, ImageFont
from decimal import Decimal,getcontext
from win32gui import FindWindow, GetWindowRect, MoveWindow
import PIL

pyt.pytesseract.tesseract_cmd = r'C:\Users\arthu\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# List of all gen 1 Pokemon names
Gen1_Pokemon = ('Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle',
           'Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto',
           'Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew',
           'Sandslash','Nidoran','Nidorina','Nidoqueen','Nidoran','Nidorino','Nidoking','Clefairy','Clefable',
           'Vulpix','Ninetales','Jigglypuff','Wigglytuff','Zubat','Golbat','Oddish','Gloom','Vileplume','Paras',
           'Parasect','Venonat','Venomoth','Diglett','Dugtrio','Meowth','Persian','Psyduck','Golduck','Mankey',
           'Primeape','Growlithe','Arcanine','Poliwag','Poliwhirl','Poliwrath','Abra','Kadabra','Alakazam','Machop',
           'Machoke','Machamp','Bellsprout','Weepinbell','Victreebel','Tentacool','Tentacruel','Geodude','Graveler',
           'Golem','Ponyta','Rapidash','Slowpoke','Slowbro','Magnemite','Magneton','Farfetch\'d','Doduo','Dodrio','Seel',
           'Dewgong','Grimer','Muk','Shellder','Cloyster','Gastly','Haunter','Gengar','Onix','Drowzee','Hypno','Krabby',
           'Kingler','Voltorb','Electrode','Exeggcute','Exeggutor','Cubone','Marowak','Hitmonlee','Hitmonchan','Lickitung',
           'Koffing','Weezing','Rhyhorn','Rhydon','Chansey','Tangela','Kangaskhan','Horsea','Seadra','Goldeen','Seaking',
           'Staryu','Starmie','Mr. Mime','Scyther','Jynx','Electabuzz','Magmar','Pinsir','Tauros','Magikarp','Gyarados',
           'Lapras','Ditto','Eevee','Vaporeon','Jolteon','Flareon','Porygon','Omanyte','Omastar','Kabuto','Kabutops',
           'Aerodactyl','Snorlax','Articuno','Zapdos','Moltres','Dratini','Dragonair','Dragonite','Mewtwo','Mew')

# Get list of all gen 1 to gen 3 pokemon moves
df = pd.read_csv('Pokemon Moves.csv')
Gens1to3_Moves = df['Name'].tolist()

# time.sleep(3)

def move_used():
    start = time.time()
    elapsed = 0
    elapsed2 = 0
    hit = True
    # pyd.press('z')
    while elapsed < 8:
        move_used_img = ImageGrab.grab(bbox=(1029, 539, 1539, 656))
        move_used = pyt.image_to_string(move_used_img)
        move_used = move_used.capitalize()
        
        if move_used.find('Wild') == 0 and 'used' in move_used and '!' in move_used:
            move_used = move_used.split('\n')[1]
            move_used = re.sub('[^a-zA-Z-]', '', move_used)
            move_used = dfl.get_close_matches(move_used,Gens1to3_Moves,cutoff=0.1)[0]
            # opp goes first ('Tackle', 1.0200340747833252) or ('Tackle', 1.1896207332611084) 
            # opp goes second after tackle ('Tackle', 3.665030002593994) 
            # opp goes second after growl ('Tackle', 5.779691219329834)
            when_used = time.time() - start
            start2 = time.time()

            while elapsed2 < 3:
                move_missed_img = ImageGrab.grab(bbox=(1029, 539, 1539, 656))
                move_missed = pyt.image_to_string(move_missed_img)
                move_missed = move_missed.capitalize()
                
                if move_used.find('Wild') != 0 and 'used' in move_used and '!' in move_used:
                   return when_used, move_used, hit

                elif ((move_missed.find('Wild') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or 
                    (move_missed.find('Wild') != 0 and ('evaded' in move_missed)) or 
                        'failed' in move_missed) and '!' in move_missed:
                    hit = False
                    return when_used, move_used, hit
                
                elapsed2 = time.time() - start2
            
            return when_used, move_used, hit

        elapsed = time.time() - start

def get_move_used():
    start = time.time()
    elapsed = 0
    elapsed2 = 0
    hit = True
    pyd.press('z')
    while elapsed < 8:
        move_used_img = ImageGrab.grab(bbox=(1029, 531, 1539, 656))
        move_used = pyt.image_to_string(move_used_img)
        move_used = move_used.capitalize()
        
        if move_used.find('Wild') != 0 and 'used' in move_used and '!' in move_used:
            # move_used_img.save('MyPokemon.jpg')
            move_used = move_used.split('\n')[1]
            move_used = re.sub('[^a-zA-Z-]', '', move_used)
            move_used = dfl.get_close_matches(move_used,Gens1to3_Moves,cutoff=0.1)[0]
            print(move_used)
            # opp goes first ('Tackle', 1.0200340747833252) or ('Tackle', 1.1896207332611084) 
            # opp goes second after tackle ('Tackle', 3.665030002593994) 
            # opp goes second after growl ('Tackle', 5.779691219329834)
            # opp attack after switch in (5.571294546127319 Tackle True)
            when_used = time.time() - start
            start2 = time.time()

            while elapsed2 < 3:
                move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                move_missed = pyt.image_to_string(move_missed_img)
                move_missed = move_missed.capitalize()
                move_missed_img.save('MyPokemon.jpg')
                
                if move_used.find('Wild') == 0 and 'used' in move_used and '!' in move_used:
                    print('1')
                    return when_used, move_used, hit

                elif move_used == 'Disable' and 'disabled' in move_missed and '!' in move_missed:
                    print('2')
                    print(move_missed)
                    move_disabled = move_missed.split('\n')[0]
                    print(move_disabled)
                    move_disabled = ' '.join(move_disabled.split()[2:])
                    print(move_disabled)
                    move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
                    print(move_disabled)
                    # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
                    return when_used, move_used, hit, move_disabled

                elif ((move_missed.find('Wild') != 0 and ('attack' in move_missed or 'missed' in move_missed)) or 
                    (move_missed.find('Wild') == 0 and ('evaded' in move_missed)) or 
                     'failed' in move_missed) and '!' in move_missed:
                    print('3')
                    hit = False
                    return when_used, move_used, hit
                
                elapsed2 = time.time() - start2
            print('4')
            return when_used, move_used, hit

        elapsed = time.time() - start

# print(get_move_used())
# pyd.press('z')
# start = time.time()
# elapsed = 0
# limit = 15
# while elapsed < limit:
#     move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656)) # change size of box
#     move_used1 = pyt.image_to_string(move_used_img)
#     move_used1 = move_used1.capitalize()
#     print(move_used1)

#     if move_used1.find('Wild') == 0 and 'disabled' in move_used1 and 'no more!' in move_used1:
#         print(move_used1)
#         print(time.time() - start)
#         print('disabled no more')

#     elapsed = time.time() - start
# print('loop done')
# print("Output: ")
# if move_used() != None and move_used()[1] == 'Move':
#     print('Output')
# else:
#     print('None!')
# print('first index')
# print(move_used[0])
# print('second index')
# print(move_used[1])
# print('third index')
# print(move_used[2])

# move_missed_img = Image.open('MyPokemon.jpg')
# # move_missed_img = move_missed_img.crop((1029, 531, 1747, 656))
# # move_missed_img.save('MyPokemon.jpg')
# move_missed = pyt.image_to_string(move_missed_img)
# move_missed = move_missed.capitalize()
# print(move_missed)
# if 'disabled' in move_missed and '!' in move_missed:
#     print('2')
#     print(move_missed)
#     move_disabled = move_missed.split('\n')[0]
#     print(move_disabled)
#     move_disabled = ' '.join(move_disabled.split()[2:])
#     print(move_disabled)
#     move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
#     print(move_disabled)
# usable_status_moves = [('apple','thelongestword',-9),('orange',1,8,21),('banana',1,3)]
# usable_status_moves.sort(key = lambda x: (len(x),abs(x[2])), reverse = True)
# for obj in usable_status_moves:
#     print(obj)

def get_color(x,y):
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgbimg = img.convert('RGB')
    return rgbimg.getpixel((0,0))

# count = 0
# red_count = 0
# for i in range(250):
#     if get_color(1297,618) != (248,0,0):
#         print('not red')
#         count += 1
#     else:
#         red_count += 1
# print(count)
# print(red_count)

# battle_over_img = ImageGrab.grab(bbox=(1029, 531, 1611, 656))
# battle_over = pyt.image_to_string(battle_over_img)
# battle_over = battle_over.capitalize()

# if 'out of' in battle_over and 'usable' in battle_over and '!' in battle_over:
#     print(battle_over)
# else:
#     print('nothing')

# print(get_color(1298,212))

def get_type_relation(typing1,typing2):
    type_relation = df2.query(f'Type==\'{typing1}\'')[typing2]
    return float(type_relation.to_string(index=False))

def get_move_type(move_name):
    get_move_type = df.query(f'Name==\'{move_name}\'')['Type']
    return get_move_type.to_string(index=False)

df2 = pd.read_csv('Type Effectiveness.csv')

# print(df2.loc['Steel']['Fighting'])
# print(get_type_relation('Steel','Fighting'))

# typing_relations = []

# move_type = get_move_type('Poison Sting')
# print(move_type)

# p = pyp.get(name='pidgey')

# for i in p.types:
#     typing_relations.append(get_type_relation(i.capitalize(),move_type))

# print(typing_relations[0] * typing_relations[1])
# count = 0
# for i in range(50):
#     if get_color(1043,533) == (40,80,104):
#         count += 1
#     else:
#         print('wrong')
# print(count)

# count = 0

# for i in range(250):
#     if get_color(1631,568) == (232,1,1):
#         count+=1
#     else:
#         print('wrong')
# print(count)

def get_pokemon_name(which_Pokemon):
        # Player Pokemon
        if which_Pokemon == 'plyr':
            # Get name in bottom left dark blue background bbox=(1029, 585, 1275, 665)
            # Get name above HP bbox=(1518, 368, 1730, 418)
            mon_name_img = ImageGrab.grab(bbox=(1518, 368, 1730, 418))
        
        elif which_Pokemon == 'slot2':
            mon_name_img = ImageGrab.grab(bbox=(1432, 132, 1633, 173))

        elif which_Pokemon == 'slot3':
            mon_name_img = ImageGrab.grab(bbox=(1432, 222, 1633, 263))

        elif which_Pokemon == 'slot4':
            mon_name_img = ImageGrab.grab(bbox=(1432, 312, 1633, 353))

        elif which_Pokemon == 'slot5':
            mon_name_img = ImageGrab.grab(bbox=(1432, 402, 1633, 443))

        elif which_Pokemon == 'slot6':
            mon_name_img = ImageGrab.grab(bbox=(1432, 492, 1633, 533))

        # Opposing Pokemon
        else:
            mon_name_img = ImageGrab.grab(bbox=(1058, 150, 1270, 198))

        thresh = 171
        fn = lambda x : 255 if x > thresh else 0
        mon_name_img = mon_name_img.convert('L').point(fn, mode='1')

        mon_name = pyt.image_to_string(mon_name_img, config='--psm 7')
        mon_name = mon_name.capitalize()

        if (mon_name.find('R. ') == 0 or mon_name.find('r. ') in (1,2)) and ('m' in mon_name or 'n' in mon_name) and 'i' in mon_name and 'e' in mon_name:
            mon_name_readjusted = 'Mr. Mime'
        
        else:
            mon_name_readjusted = re.sub('[^a-zA-Z]', '', mon_name)

        return dfl.get_close_matches(mon_name_readjusted,Gen1_Pokemon,cutoff=0.1)[0]

# print(get_pokemon_name('plyr'))

def get_pokemon_level(which_Pokemon):
    if which_Pokemon == 'plyr':
        mon_lvl_img = ImageGrab.grab(bbox=(1735, 368, 1838, 415))

    else:
        mon_lvl_img = ImageGrab.grab(bbox=(1275, 150, 1378, 198))
    
    thresh = 171
    fn = lambda x : 255 if x > thresh else 0
    mon_lvl_img = mon_lvl_img.convert('L').point(fn, mode='1')

    mon_lvl = pyt.image_to_string(mon_lvl_img, config='--psm 10')
    
    mon_lvl = mon_lvl[2:]
    mon_lvl = mon_lvl.lower()
    
    mon_lvl = mon_lvl.replace('la','14')
    mon_lvl = mon_lvl.replace('?','7')
    mon_lvl = mon_lvl.replace('s','5')
    mon_lvl = mon_lvl.replace('d','4')
    mon_lvl = mon_lvl.replace('l','1')
    mon_lvl = mon_lvl.replace('i','1')
    mon_lvl = mon_lvl.replace('o','0')
    
    if len(mon_lvl) > 2 and '00' not in mon_lvl:
        mon_lvl = mon_lvl[1:]
        
    mon_lvl = re.sub('[^\d]', '', mon_lvl)

    if mon_lvl == '':
        return 'empty'
    else:
        return mon_lvl

def get_pokemon_move(which_move):
    if which_move == 1:
        move_img = ImageGrab.grab(bbox=(1050, 540, 1310, 590))
        
    elif which_move == 2:
        move_img = ImageGrab.grab(bbox=(1315, 540, 1575, 590))
        
    elif which_move == 3:
        move_img = ImageGrab.grab(bbox=(1050, 600, 1310, 650))
        
    else:
        move_img = ImageGrab.grab(bbox=(1315, 600, 1575, 650))
    
    move_name = pyt.image_to_string(move_img, config='--psm 7')
    move_name = move_name.capitalize()
    
    move_name_readjusted = re.sub('[^a-zA-Z-]', '', move_name)

    if move_name_readjusted == '' or move_name_readjusted == '-':
        return 'empty'

    return which_move,dfl.get_close_matches(move_name_readjusted,Gens1to3_Moves,cutoff=0.1)[0]

# my_mon = get_pokemon_name('plyr')
# my_mon_lvl = get_pokemon_level('plyr')
# my_stat_stages = [0,0,0,0,0]
# opp_mon = get_pokemon_name('opp')
# opp_mon_lvl = get_pokemon_level('opp')
# opp_stat_stages = [0,0,0,0,0]
# print(my_mon)
# print(my_mon_lvl)
# print(opp_mon)
# print(opp_mon_lvl)

# my_moves = []
# for i in range(1,5):
#     move = get_pokemon_move(i)
#     if move != 'empty':
#         my_moves.append(move)

# usable_moves = []

# for i in range(len(my_moves)):
#     usable_moves.append((my_moves[i][0],my_moves[i][1],calc_move(my_mon,my_mon_lvl,'18',my_stat_stages,opp_mon,opp_mon_lvl,'31',opp_stat_stages,my_moves[i][1])[0]))
    
# usable_moves.sort(key = lambda x: x[2], reverse = True)
# print(usable_moves)
# stat1 = [0,0,0,0,0]
# stat2 = [0,0,0,0,0]
# print(calc_move('Nidoran-F','6','18',stat1,'Chansey','3','31',stat2,'Fire Punch')[0])
# print(get_pokemon_level('plyr'))

# p = pyp.get(name='Nidoran-F')
# print(p.types)
# string = 'apple'
# x = string.split(' ')
# print(x)

df3 = pd.read_csv('Pokemon Types.csv')

def get_mon_type(mon_name):
    mon_type = df3.query(f'Name==\'{mon_name}\'')['Type']
    return mon_type.to_string(index=False).split(' ')

# for i in get_mon_type('Poliwrath'):
#     print(i)

# get_color(1170,385) == (69,161,155)
# get_color(1029,437) == (32,104,96)
# get_color(1867,135) == (56,144,216)
# start = time.time()
# pyd.press('z')
# while True:
#     if get_color(1867,135) == (56,144,216):
#         print(time.time()-start)
#         break

# type_cover1 = df2['Poison'].tolist()
# type_cover2 = df2['Grass'].tolist()
# type_cover = []

# for i in range(len(type_cover1)):
#     if type_cover1[i] >= type_cover2[i]:
#         type_cover.append(type_cover1[i])
#     else:
#         type_cover.append(type_cover2[i])
# print(type_cover)

# cover_sum = 0

# for i in type_cover:
#     cover_sum += i

# print(cover_sum)

    # start = time.time()
    # elapsed = 0
    # elapsed2 = 0
    # hit = True

    # while elapsed < 15:
    #     if get_color(1297,618) == (248,0,0):
    #         pyd.press('z')
    #     else:
    #         move_used_img = ImageGrab.grab(bbox=(1029, 531, 1539, 656))
    #         move_used = pyt.image_to_string(move_used_img)
    #         move_used = move_used.capitalize()
            
    #         if 'fainted' in move_used or 'potion' in move_used or 'full restore' in move_used:
    #             return None
    #         elif move_used.find('Foe') == 0 and 'used' in move_used and '!' in move_used:
    #             move_used = move_used.split('\n')[1]
    #             move_used = re.sub('[^a-zA-Z-]', '', move_used)
    #             move_used = dfl.get_close_matches(move_used,Gens1to3_Moves,cutoff=0.1)[0]
    #             # opp goes first ('Tackle', 1.0200340747833252) or ('Tackle', 1.1896207332611084) 
    #             # opp goes second after tackle ('Tackle', 3.665030002593994) 
    #             # opp goes second after growl ('Tackle', 5.779691219329834)
    #             # opp attack after switch in (5.571294546127319 Tackle True)
    #             when_used = time.time() - start
    #             start2 = time.time()

    #             while elapsed2 < 3:
    #                 move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
    #                 move_missed = pyt.image_to_string(move_missed_img)
    #                 move_missed = move_missed.capitalize()
                    
    #                 if move_missed.find('Foe') != 0 and 'used' in move_missed and '!' in move_missed:
    #                     return when_used, move_used, hit
                    
    #                 elif move_used == 'Disable' and 'disabled' in move_missed and '!' in move_missed:
    #                     move_disabled = move_missed.split('\n')[0]
    #                     move_disabled = ' '.join(move_disabled.split()[1:])
    #                     move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
    #                     # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
    #                     return when_used, move_used, hit, move_disabled
                    
    #                 elif ((move_missed.find('Foe') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or 
    #                     (move_missed.find('Foe') != 0 and ('evaded' in move_missed)) or 
    #                     'failed' in move_missed) and '!' in move_missed:
    #                     hit = False
    #                     return when_used, move_used, hit
                    
    #                 elapsed2 = time.time() - start2
                
    #             return when_used, move_used, hit

    #     elapsed = time.time() - start

# move_used_img = Image.open(r'C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-08-22 013415.png')
# move_used_img = move_used_img.crop((1029, 531, 1747, 656))
# move_used1 = pyt.image_to_string(move_used_img)
# move_used1 = move_used1.capitalize()
# print(move_used1)

# if 'paralyzed!' in move_used1 and 'it can’t move!' in move_used1:
#     print(True)
# else:
#     print(False)

def get_move_used(check_my_move,check_status_move,my_move_name):
    start = time.time()
    elapsed = 0
    elapsed2 = 0
    elapsed3 = 0
    opp_mon_attack = True
    disable_check = False
    hit = True
    my_move_went = True
    my_mon_attack = False
    search_again = ''

    if check_my_move == True:
        if my_move_name == 'Bounce':
            search_for = 'sprang up'
        elif my_move_name == 'Dig':
            search_for = 'dug a hole'
        elif my_move_name == 'Dive':
            search_for = 'hid'
            search_again = 'underwater'
        elif my_move_name == 'Fly':
            search_for = 'flew'
            search_again = 'high'
        elif my_move_name == 'Razor Wind':
            search_for = 'up'
            search_again = 'whirlwind'
        elif my_move_name == 'Skull Bash':
            search_for = 'lowered'
            search_again = 'head'
        elif my_move_name == 'Sky Attack':
            search_for = 'glowing'
        elif my_move_name == 'SolarBeam':
            search_for = 'took'
            search_again = 'sunlight'

    if check_my_move or check_status_move:
        limit = 15
    else:
        limit = 3

    while elapsed < 15:
        if get_color(1297,618) == (248,0,0):
            pyd.press('z')
        else:
            move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
            move_used = pyt.image_to_string(move_used_img)
            move_used = move_used.capitalize()
            
            if check_my_move:
                if move_used.find('Wild') != 0 and (('paralyzed!' in move_used and 'it can’t move!' in move_used) or 
                ('is fast' in move_used and 'asleep' in move_used) or ('used' in move_used)):
                    my_move_went = False
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
                elif move_used.find('Wild') != 0 and (search_for in move_used and search_again in move_used):
                    my_move_went = True
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
            if check_status_move:
                if move_used.find('Wild') != 0 and (('paralyzed!' in move_used and 'it can’t move!' in move_used) or 
                ('is fast' in move_used and 'asleep' in move_used)):
                    my_move_went = False
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
                elif move_used.find('Wild') != 0 and 'used' in move_used:
                    my_mon_attack = True
                    start3 = time.time()
                    while elapsed3 < 8:
                        status_move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                        status_move_missed = pyt.image_to_string(status_move_missed_img)
                        status_move_missed = status_move_missed.capitalize()
                        
                        if (status_move_missed.find('Wild') != 0 and ('attack' in status_move_missed or 'missed' in status_move_missed)) or \
                        (status_move_missed.find('Wild') == 0 and ('evaded' in status_move_missed)) or \
                        'failed' in status_move_missed or (status_move_missed.find('Foe') == 0 and 'soundproof' in status_move_missed and 'blocks' in status_move_missed):
                            my_move_went = False
                            break

                        elif 'fell' in status_move_missed or 'rose' in status_move_missed:
                            my_move_went = True
                            break

                        elasped3 = time.time() - start3

                    if opp_mon_attack == False:
                        return None, my_move_went
                        
            if 'fainted' in move_used or 'potion' in move_used or 'full restore' in move_used or (move_used.find('Wild') == 0 
                and (('paralyzed!' in move_used and 'it can’t move!' in move_used) or ('is fast' in move_used and 'asleep' in move_used))):
                opp_mon_attack = False
                if check_my_move == False and check_status_move == False:
                    return None
                elif my_mon_attack == True:
                    return None, my_move_went
            elif move_used.find('Wild') == 0 and 'used' in move_used and '!' in move_used:
                move_used = move_used.split('\n')[1]
                move_used = re.sub('[^a-zA-Z-]', '', move_used)
                move_used = dfl.get_close_matches(move_used,Gens1to3_Moves,cutoff=0.1)[0]
                # opp goes first ('Tackle', 1.0200340747833252) or ('Tackle', 1.1896207332611084) 
                # opp goes second after tackle ('Tackle', 3.665030002593994) 
                # opp goes second after growl ('Tackle', 5.779691219329834)
                # opp attack after switch in (5.571294546127319 Tackle True)
                when_used = time.time() - start
                start2 = time.time()

                while elapsed2 < limit:
                    move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                    move_missed = pyt.image_to_string(move_missed_img)
                    move_missed = move_missed.capitalize()
                    
                    if move_missed.find('Wild') != 0 and 'used' in move_missed and '!' in move_missed:
                        if check_my_move == False and check_status_move == False:
                            return when_used, move_used, hit
                        elif my_mon_attack == True:
                            return when_used, move_used, hit, my_move_went
                    
                    elif move_used == 'Disable' and 'disabled' in move_missed and '!' in move_missed:
                        move_disabled = move_missed.split('\n')[0]
                        move_disabled = ' '.join(move_disabled.split()[1:])
                        move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
                        disable_check = True
                        # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
                        if (check_my_move == True or check_status_move == True) and move_disabled == my_move_name:
                            my_move_went = False
                            return when_used, move_used, hit, move_disabled, my_move_went
                        elif check_my_move == False:
                            return when_used, move_used, hit, move_disabled
                    
                    elif (move_missed.find('Wild') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or \
                        (move_missed.find('Wild') != 0 and ('evaded' in move_missed)) or \
                        'failed' in move_missed:
                        hit = False
                        if check_my_move == False:
                            return when_used, move_used, hit
                        elif my_mon_attack == True:
                            return when_used, move_used, hit, my_move_went
                    
                    if check_my_move == True and my_mon_attack == False:
                        if move_missed.find('Wild') != 0 and (('paralyzed!' in move_missed and 'it can’t move!' in move_missed) 
                        or ('is fast' in move_missed and 'asleep' in move_missed) or 
                        ('used' in move_missed) or 'fainted' in move_missed):
                            my_move_went = False
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                        elif move_missed.find('Wild') != 0 and (search_for in move_missed and search_again in move_missed):
                            my_move_went = True
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                    
                    if check_status_move == True and my_mon_attack == False:
                        if move_missed.find('Wild') != 0 and (('paralyzed!' in move_missed and 'it can’t move!' in move_missed) or 
                        ('is fast' in move_missed and 'asleep' in move_missed) or 'fainted' in move_missed):
                            my_move_went = False
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                        elif move_missed.find('Wild') != 0 and 'used' in move_missed:
                            my_mon_attack = True
                            start3 = time.time()
                            while elapsed3 < 8:
                                print('checking my move')
                                status_move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                                status_move_missed = pyt.image_to_string(status_move_missed_img)
                                status_move_missed = status_move_missed.capitalize()
                                
                                if (status_move_missed.find('Wild') != 0 and ('attack' in status_move_missed or 'missed' in status_move_missed)) or \
                                (status_move_missed.find('Wild') == 0 and ('evaded' in status_move_missed)) or \
                                'failed' in status_move_missed or (status_move_missed.find('Foe') == 0 and 'soundproof' in status_move_missed and 'blocks' in status_move_missed):
                                    my_move_went = False
                                    break

                                elif 'fell' in status_move_missed or 'rose' in status_move_missed:
                                    my_move_went = True
                                    break

                                elasped3 = time.time() - start3
                                print(elasped3)
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went

                    elapsed2 = time.time() - start2
                    
                if check_my_move or check_status_move:
                    return when_used, move_used, hit, my_move_went
                else:
                    return when_used, move_used, hit

        elapsed = time.time() - start

def get_move_used2(starting,disabled_move):
    start = starting
    elapsed = 0
    hit = True
    disable_off = False

    move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
    move_used = pyt.image_to_string(move_used_img)
    move_used = move_used.capitalize()
    
    if get_color(1297,618) == (248,0,0):
        pyd.press('z')
        
    elif move_used.find('Wild') != 0 and 'disabled' in move_used and 'no more!' in move_used:
        disable_off = True
        
    elif 'fainted' in move_used or 'potion' in move_used or 'full restore' in move_used or (move_used.find('Wild') == 0 
        and (('paralyzed!' in move_used and 'it can’t move!' in move_used) or ('is fast' in move_used and 'asleep' in move_used))):
        if disabled_move != '':
            return None, disable_off
        return None
    elif move_used.find('Wild') == 0 and 'used' in move_used and '!' in move_used:
        move_used = move_used.split('\n')[1]
        move_used = re.sub('[^a-zA-Z-]', '', move_used)
        move_used = dfl.get_close_matches(move_used,Gens1to3_Moves,cutoff=0.1)[0]
        # opp goes first ('Tackle', 1.0200340747833252) or ('Tackle', 1.1896207332611084) 
        # opp goes second after tackle ('Tackle', 3.665030002593994) 
        # opp goes second after growl ('Tackle', 5.779691219329834)
        # opp attack after switch in (5.571294546127319 Tackle True)
        when_used = time.time() - start
        start2 = time.time()

        while elapsed < 3:
            move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
            move_missed = pyt.image_to_string(move_missed_img)
            move_missed = move_missed.capitalize()
            
            if move_missed.find('Wild') != 0 and 'disabled' in move_missed and 'no more!' in move_missed:
                disable_off = True

            elif move_missed.find('Wild') != 0 and 'used' in move_missed and '!' in move_missed:
                if disabled_move != '':
                    return when_used, move_used, hit, disable_off
                return when_used, move_used, hit
            
            elif move_used == 'Disable' and 'disabled' in move_missed and '!' in move_missed:
                move_disabled = move_missed.split('\n')[0]
                move_disabled = ' '.join(move_disabled.split()[1:])
                move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
                # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
                if disabled_move != '':
                    return when_used, move_used, hit, move_disabled, disable_off
                return when_used, move_used, hit, move_disabled
            
            elif ((move_missed.find('Wild') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or 
                (move_missed.find('Wild') != 0 and ('evaded' in move_missed)) or 
                'failed' in move_missed) and '!' in move_missed:
                hit = False
                if disabled_move != '':
                    return when_used, move_used, hit, disable_off
                return when_used, move_used, hit
            
            elapsed = time.time() - start2
        if disabled_move != '':
            return when_used, move_used, hit, disable_off
        return when_used, move_used, hit
    return ''

# check_my_move = False
# check_status_move = True
# pyd.press('z')
# opp_move_used = get_move_used(check_my_move,check_status_move,'Tail Whip')
# print(opp_move_used)

# keep_checking = True
# opp_move_used2 = ''
# disabled_move = 'something'
# # disabled red arrow
# while get_color(1491,516) != (208,160,208) and get_color(1098,201) == (248,248,216) and get_color(1525,431) == (248,248,216):
#     if check_my_move == True and keep_checking == True and ((len(opp_move_used) == 2 and opp_move_used[1] == True) or (len(opp_move_used) == 4 and
#         opp_move_used[3] == True) or (len(opp_move_used) == 5 and opp_move_used[4] == True)):
#         starting = time.time()
#         while opp_move_used2 == '':
#             opp_move_used2 = get_move_used2(starting,disabled_move)
#         print(opp_move_used2)
#         keep_checking = False
            
#         if disabled_move != '':
#             if len(opp_move_used2) == 2:
#                 if opp_move_used2[1] == True:
#                     disabled_move = ''

#             elif len(opp_move_used2) == 4:
#                 if opp_move_used2[3] == True:
#                     disabled_move = ''
            
#             elif len(opp_move_used2) == 5:
#                 if opp_move_used2[4] == True:
#                     disabled_move = ''

# damage: [
#     137, 139, 140, 142,
#     144, 145, 147, 149,
#     150, 152, 153, 155,
#     157, 158, 160, 162
#   ],

def calc_move(atk_mon,atk_lvl,atk_ivs,atk_mon_stages,def_mon,def_lvl,def_ivs,def_mon_stages,reflect_on,lightscreen_on,status_atk,status_def,HP_amount,move,max_min):
    atk_stat1 = str(atk_mon_stages[0])
    spa_stat1 = str(atk_mon_stages[2])
    spe_stat1 = str(atk_mon_stages[4])

    def_stat2 = str(def_mon_stages[1])
    spd_stat2 = str(def_mon_stages[3])
    spe_stat2 = str(def_mon_stages[4])
    
    process = subprocess.check_output(['node','PokemonDamageCalculator\Pokemon_Damage_Calculator.mjs',atk_mon,atk_lvl,atk_ivs,atk_stat1,spa_stat1,spe_stat1,def_mon,def_lvl,def_ivs,def_stat2,spd_stat2,spe_stat2,reflect_on,lightscreen_on,status_atk,status_def,HP_amount,move,max_min])
    process = process.decode("utf-8").replace('\n','').split(' ')
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

# print(calc_move('Gengar','100','31',[0,0,0,0,0],'Chansey','100','31',[0,0,0,0,0],'false','true','par','par','100','Water Spout','max'))

# load image
img1 = Image.open(r'C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-08-19 150255.png').convert('RGB')
image = img1.crop((1581,583,1890,628))
# output = pyt.image_to_string(image, config='--psm 7')
# print(output)
# inv_img = ImageOps.invert(image)
# inv_img.show() #1581,583,1890,628 #1122,150,1389,208
img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# define range wanted color in HSV
lower_val = np.array([0,0,0]) 
upper_val = np.array([145,145,145])
# 85,85,85 65,175,85 name 125 125 125 129 129 129 131 131 131 145 145 145 116 116 116 last move name
# Threshold the HSV image - any green color will show up as white
mask = cv2.inRange(hsv, lower_val, upper_val)
pil_image = Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
# pil_image.show()
output = pyt.image_to_string(pil_image, config='--psm 7')
# print(output)

# if there are any white pixels on mask, sum will be > 0
# hasGreen = np.sum(mask)
# if hasGreen > 0:
#     print('Red detected!')
# res = cv2.bitwise_and(img,img,mask=mask)
# fin = np.hstack((img,res))
# # display image
# cv2.imshow("Res", fin)
# cv2.imshow("Mask", mask)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# color = np.uint8([[[36,85,55]]])
# color_convert = cv2.cvtColor(color,cv2.COLOR_BGR2HSV)
# color_convert = cv2.cvtColor(color,cv2.COLOR_HSV2BGR)
# print(color_convert)
# 146,82,125 146 255 255
# check for disable, reflect, light screen
# none if opp is immobilized
# get the move(s) the opp used
    # whether it hits or not
# if checking for status move
    # whether it hits or not
# continue the loop if my mon faints
    # check for red arrow and press 'z'
    # look for move
        # if opp used status move (on itself), add it to stat changes
    # break if lose battle
# break if the opp faints

def get_move_score(move_name):
    move_power = df.query(f'Name==\'{move_name}\'')['Power']
    move_power = int(move_power.to_string(index=False))
    move_acc = df.query(f'Name==\'{move_name}\'')['Accuracy']
    move_acc = move_acc.to_string(index=False)
    if move_acc == 'NaN':
        move_acc = 101
    else:
        move_acc = int(move_acc[:-1])
    return(move_power,move_acc)

# print(get_move_score('Earthquake'))

move_power = 80
move_acc = 100
# print(((move_acc/100) * (((move_acc/100)/0.65) ** 1.25)) + ((move_power/100) * (((move_power/100)/0.5) ** 0.3)))
# opp_move_used = [None,['apple','orange'],['apple2','orange2'],['apple3','orange3']]
# for i in opp_move_used:
#     if i != None and 'NoAdd' not in i:
#         i.append('NoAdd')
# print(opp_move_used)
# time.sleep(2.5)
# count = 0
# for i in range(50):
#     which_my_status = get_color(1537,457)
#     if which_my_status == (192,96,192):
#         count += 1
# print(count)

# count = 0
# for i in range(50):
#     which_my_status = get_color(1537,457)
#     if which_my_status == (192,96,192):
#         count += 1
# print(count)
# count = 0
# prev_length = 50
# elapsed = 0
# start = time.time()
# pyd.press('z')
# while elapsed < 10:
#     move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
#     move_used1 = pyt.image_to_string(move_used_img)
#     move_used1 = move_used1.capitalize()
#     if len(move_used1) < prev_length:
#         different_text = True
#         print('compare: ' + str(len(move_used1)))
#         print('compare: ' + str(prev_length))
#     prev_length = len(move_used1)
#     # print('this is ' + str(prev_length))
#     # print('text ' + move_used1)

#     if 'apple' in move_used1:
#         pass

#     elif 'orange' in move_used1:
#         pass

#     elif 'square' in move_used1:
#         pass
    
#     elif 'triangle' in move_used1:
#         pass

#     elif move_used1.find('Wild') == 0 and 'used' in move_used1 and '!' in move_used1 and different_text == True:
#         count += 1
#         different_text = False
#         elapsed2 = 0
#         start2 = time.time()
#         while elapsed2 < 3:
#             move_used_img2 = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
#             move_used2 = pyt.image_to_string(move_used_img2)
#             move_used2 = move_used2.capitalize()
#             move_used2.capitalize()
#             prev_length = len(move_used2)

#             if move_used2.find('Wild') != 0 and 'used' in move_used2:
#                 # different_text = True
#                 break
#             # elif 'rattata’s' in move_used2:
#             #     print('move missed')
#             #     break
#             elapsed2 = time.time() - start2
#         # print('inside text: ' + str(prev_length))
#     elif move_used1.find('Wild') != 0 and 'used' in move_used1 and '!' in move_used1 and different_text == True:
#         # print('my turn')
#         count += 1
#         different_text = False
    
#     elapsed = time.time() - start

# print(count)
# text = 'Ditto transformed \ninto Venusaur!'
# print(text)
# text = text.split()[-1:][0][:-1]
# print(text)
# C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-09-09 221747.png
# # image1 = Image.open(r'C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-08-22 013415.png').convert('RGB')
# image1 = Image.open(r'C:\Users\arthu\Pictures\Screenshots\FireRed Font.bmp').convert('RGB')
# # image1 = image1.crop((1029, 531, 1747, 656))
# image1 = ImageOps.invert(image1)
# # image1.show()
# image1.save('FireRed Font.png')
# # move_used1 = pyt.image_to_string(image1,lang='train')
# # move_used1 = move_used1.capitalize()
# # print(move_used1)
# start = time.time()
# time.sleep(3)
# pyd.press('left')
# pyd.press('down')
# pyd.press('up')
# if get_color(1631,568) == (232,1,1):
#     print('no pp')
# else:
#     print('pp')
# # print(time.time() - start)
# breakpoint()
import mss
# start = time.time()
# for i in range(10):
#     with mss.mss() as sct:
#         img = sct.grab((1029, 531, 1747, 655))
#         img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
#         img = img.resize((460, 125))
#         # img.show()
# print(time.time() - start)
# # start = time.time()
# # img = ImageGrab.grab((1029, 531, 1747, 655))
# # # img = img.resize((460, 125))
# # # img.show()
# # print(time.time() - start)
# breakpoint()

# with mss.mss() as sct:
#     mon_name_img = sct.grab((1058, 150, 1270, 198))
#     # mon_name_img = sct.grab((1518, 368, 1730, 418))
#     mon_name_img = cv2.cvtColor(np.array(mon_name_img), cv2.COLOR_BGRA2BGR)
#     # mon_name_img = Image.fromarray(cv2.cvtColor(np.array(mon_name_img), cv2.COLOR_BGRA2RGB))
#     mask = np.all((mon_name_img <= [150, 150, 150]), axis=-1)
#     mon_name_img[mask] = [255, 255, 255]
#     mon_name_img[~mask] = [0, 0, 0]
#     mon_name_img = Image.fromarray(cv2.cvtColor(mon_name_img, cv2.COLOR_BGR2RGB))
#     # thresh = 171
#     # fn = lambda x : 255 if x > thresh else 0
#     # mon_name_img = mon_name_img.convert('L').point(fn, mode='1')
#     mon_name_img.show()
# import pyautogui as pyg
# print(pyg.position())

# time.sleep(1.5)
# with mss.mss() as sct:
#     no_moves_img = sct.grab((1029, 531, 1747, 655))
#     no_moves = pyt.image_to_string(np.array(no_moves_img))
#     print(no_moves)

# while True:
#     with mss.mss() as sct:
#         img = sct.grab((1029, 531, 1747, 655))
#         img = Image.frombytes('RGB', img.size, img.bgra, 'raw', 'BGRX')
#         img = img.resize((460, 125))
#         img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#         mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 255])), axis=-1)
#         img[mask] = [0, 0, 0]
#         img[~mask] = [255, 255, 255]
#         # img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         # img.show()
#         battle_text = pyt.image_to_string(img, lang='FireRedVer1')
#         battle_text = '\n'.join([ll.rstrip() for ll in battle_text.splitlines() if ll.strip()])
#         print(battle_text)
        # print(pyt.image_to_string(img,lang='FireRedver1'))
        # break
# breakpoint()
# path = r'C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images'
# img = Image.open(path + '\FireRed Font20.png')

# test geodude is paralyzed and Wild Rattata's attack missed and Wild Pidgey used Tackle
start = time.time()
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-10-26 184204.png") # Wild PIDGEY used TACKLE!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-08-22 013415.png") # Geodude is paralyzed! It can't move!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-08-09 160711.png") # Wild RATTATA's attack missed!
# img = Image.open(r'C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-09 221747.png') # " "' ''s SPEED fell!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-08-10 222527.png") # Bug CATCHER Rick would like to battle! v
img = Image.open(r'C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-09 222054.png') # UVWXYZ.,!? immobilized by love!
# img = Image.open(r'C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-09 222311.png') # Wild Pikachu's accuracy fell!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-10 015617.png") # BULBASAUR got an ENCORE!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-10 013730.png") # Foe EKANS's INTIMIDATE cuts JIGGLYPUFF's ATTACK!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-10-28 024735.png") # GEODUDE used DIG!
# img = Image.open(r'C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-10-28 025945.png') # GEODUDE used DIG (prc)!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-10 013956.png") # Wild NIDORAN-M appeared!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-10 014540.png") # Wild NIDORAN-F used GROWL!
# img = Image.open(r"C:\Users\arthu\Pictures\FireRedTesseractTraining\Training Images (Unedited)\Screenshot 2023-09-09 222207.png") # AAAAAAA got $224 for winning!
# img = img.crop((1029, 530, 1747, 655))
img = img.crop((1029, 531, 1747, 655))
# img = img.crop((1025, 531, 1747, 656))
# img1 = img
# battle_text = pyt.image_to_string(img)
# print(battle_text)
# breakpoint()
img = img.resize((460, 125))
# img = img.resize((380, 100)) # <- removes empty new line and space before the last ! (combine with img <= [150, 150, 150])
# img.show()
# img = cv2.imread(path + '\FireRed Font29.png')
# with mss.mss() as sct:
#     img = sct.grab((1025, 531, 1747, 656))
# img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
# mask = np.all((img <= [165, 165, 165]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
# mask = np.all((img <= [160, 160, 160]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
# mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
# mask = np.all((img <= [140, 140, 140]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1) # <- reduces space from ! best
mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 255])), axis=-1) # <- best one to use (better than 140) when combining with image
# # img = cv2.imread(r'C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-10-26 181940.png')
# # mask = np.all((img <= [170, 170, 170]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
img[mask] = [0, 0, 0]
img[~mask] = [255, 255, 255]
img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# # 40 80 104
# img.show()
# img.save('img1.tiff')
# battle_text = pyt.image_to_string(img, lang='FireRedVer0')
battle_text = pyt.image_to_string(img, lang='FireRedVer1')
# print(battle_text.splitlines())
battle_text = '\n'.join([ll.rstrip() for ll in battle_text.splitlines() if ll.strip()])
# print(time.time() - start)
print(battle_text)
# print(pyt.image_to_string(img))
breakpoint()

def continue_text(img, isRGB):
    if isRGB:
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower_val = np.array([0,100,100])
    # upper_val = np.array([255,255,0])
    # mask = cv2.inRange(hsv, lower_val, upper_val)
    mask = np.all((img >= [53, 41, 142] & (img <= [0, 0, 248])), axis=-1)
    img[mask] = [255, 255, 255]
    img = Image.fromarray(cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB))
    img.show()
    hasRed = np.sum(mask)
    # res = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('img', res)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if hasRed > 0:
        return True
    else:
        return False
# print(continue_text(img, False))
# breakpoint()
path = r'C:\Users\arthu\Pictures\FireRedTesseractTraining\FireRedTrainingImages2'
# path = r'C:\Users\arthu\Pictures\Training Images (Unedited)'
dir_list = os.listdir(path)
# num = 1
# # widthlist = []
# for i in dir_list:
#     if i != 'desktop.ini':
#         img = Image.open(r'C:\Users\arthu\Pictures\Training Images (Unedited)\\' + i)
#         img = img.crop((1029, 531, 1747, 655))
#         img = img.resize((460, 125))
#         # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
#         img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#         mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 255])), axis=-1)
#         img[mask] = [0, 0, 0]
#         img[~mask] = [255, 255, 255]
#         img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#         img.save(f'FireRed Font{num}.png')
#         num += 1
#         # widthlist.append(cv2.imread(r'C:\Users\arthu\Pictures\Saved Pictures\\' + i).shape[1])
# # maxwidth = max(widthlist)
# breakpoint()
imgs = []
dir_list2 = []
for i in dir_list:
    if i == 'FireRed Font.png':
        i = 'FireRed Font1.png'

    if i != 'desktop.ini':
        dir_list2.append(i)
dir_list2.sort(key = lambda x: int(x[12:][:-4]))
# print(dir_list2)

for i in dir_list2:
    if i == 'FireRed Font1.png':
        i = 'FireRed Font.png'
    if i != 'desktop.ini':
        img = Image.open(r'C:\Users\arthu\Pictures\FireRedTesseractTraining\FireRedTrainingImages2\\' + i)
        # img = img.resize((618, 125))
        # img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # mask = np.all((img <= [150, 150, 150]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
        # mask = np.all((img <= [170, 170, 170]) | ((img >= [53, 41, 142]) & (img <= [0, 0, 248])), axis=-1)
        # img[mask] = [0, 0, 0]
        # img[~mask] = [255, 255, 255]
        # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        # img = ImageOps.invert(img)
        img = np.array(img)
        # image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # image[np.where((image==[151, 175, 215]).all(axis=2))] = [255, 255, 255]
        # color_converted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # img = Image.fromarray(color_converted)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        # img = cv2.copyMakeBorder(img, 0, 0, 0, maxwidth-img.shape[1], borderType=cv2.BORDER_CONSTANT, value=(0,0,0,0))
        imgs.append(img)
# result = cv2.vconcat(imgs)
imageio.mimwrite('FireRed Training Font.tiff', imgs)
breakpoint()
# # img = Image.open(r'C:\Users\arthu\Documents\Programming\Python_MyProjects\PokemonFireRedAI\FireRed Training Font.png').convert('RGB')
# # img = ImageOps.invert(img)
# # img.save('FireRed Training Font.png')
# ‘ ’ “ ” ♂ ♀
# import csv
# import textwrap

# width = 950
# height = 880
# font = ImageFont.truetype("pokemon_fire_red.ttf", size=60)

# with open('Pokemon Text.csv', 'r', encoding="utf8") as f:
#     reader = csv.reader(f)
#     i = 0
#     for [message] in reader:
#         i += 1
#         listoftext = message.split(' ')
#         if i >= 1 and i <= 151:
#             message = listoftext[0].upper() + '’s'
#         if i == 152:
#             listoftext.append(' ,')
#             message = ' '.join(listoftext)
#         if i >= 153:
#             listoftext[1] = listoftext[1].upper()
#             listoftext[2] = listoftext[2].upper()
#             message = ' '.join(listoftext)
#         img = Image.new('RGB', (width, height), color='white')
#         draw = ImageDraw.Draw(img)
#         image_width, image_height = image.size
#         y_text = 10
#         lines = textwrap.wrap(message, width=45)
#         for line in lines:
#             line_width, line_height = font.getsize(line)
#             draw.text((10, y_text), line, font=font, fill=(0,0,0))
#             y_text += line_height + 10
#         img.save(f'FireRed Font{i}.png')

df = pd.read_csv('Pokemon Moves.csv')
Gens1to3_Moves = df['Name'].tolist()

df2 = pd.read_csv('Pokemon Types.csv')

df3 = pd.read_csv('Type Effectiveness.csv')

status_moves = {
    'Swords Dance': (2,'atk','user'),
    'Tail Whip': (-1,'def','target'),
    'Leer': (-1,'def','target'),
    'Growth': (1,'spa','user'),
    'String Shot': (-1,'spe','target'),
    'Meditate': (1,'atk','user'),
    'Agility': (2,'spe','user'),
    'Screech': (-2,'def','target'),
    'Harden': (1,'def','user'),
    'Withdraw': (1,'def','user'),
    'Defense Curl': (1,'def','user'),
    'Barrier': (2,'def','user'),
    'Skull Bash': (1,'def','user'),
    'Amnesia': (2,'spd','user'),
    'Acid Armor': (2,'def','user'),
    'Sharpen': (1,'atk','user'),
    'Curse': (1,'atk',1,'def',-1,'spe','user'),
    'Cotton Spore': (-2,'spe','target'),
    'Scary Face': (-2,'spe','target'),
    'Belly Drum': (6,'atk','user'),
    'Icy Wind': (-1,'spe','target'),
    'Charm': (-2,'atk','target'),
    'Swagger': (2,'atk','target'),
    'Stockpile': (1,'def',1,'spd','user'),
    'Flatter': (1,'spa','target'),
    'Memento': (-2,'atk',-2,'spa','target'),
    'Superpower': (-1,'atk',-1,'def','user'),
    'Tail Glow': (2,'spa','user'),
    'FeatherDance': (-2,'atk','target'),
    'Fake Tears': (-2,'spd','target'),
    'Overheat': (-2,'spa','user'),
    'Rock Tomb': (-1,'spe','target'),
    'Metal Sound': (-2,'spd','target'),
    'Tickle': (-1,'atk',-1,'def','target'),
    'Cosmic Power': (1,'def',1,'spd','user'),
    'Iron Defense': (2,'def','user'),
    'Howl': (1,'atk','user'),
    'Bulk Up': (1,'atk',1,'def','user'),
    'Mud Shot': (-1,'spe','target'),
    'Calm Mind': (1,'spa',1,'spd','user'),
    'Dragon Dance': (1,'atk',1,'spe','user'),
    'Psycho Boost': (-2,'spa','user')
}

hwnd = FindWindow(None,'VisualBoyAdvance')
MoveWindow(hwnd,791,15,736,539,True)

physical_types = ['Normal','Fighting','Poison','Ground','Flying','Bug','Rock','Ghost','Steel']

def get_move_type(move_name):
    get_move_type = df.query(f'Name==\'{move_name}\'')['Type']
    return get_move_type.to_string(index=False)

def get_mon_type(mon_name):
    mon_type = df2.query(f'Name==\'{mon_name}\'')['Type']
    return mon_type.to_string(index=False).split(' ')

def get_type_relation(typing1,typing2):
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

def get_move_score(move_name,move1,move2,move3,move4,mon,learned):
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
    if move_name in ('Selfdestruct','Explosion','Memento'):
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
                    for i in (move1,move2,move3,move4):
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
                    score += min(boost,4.5)
                elif (status_moves[move_name][0] > 0 and status_moves[move_name][1] == 'spa' and status_moves[move_name][2] == 'user') \
                or (status_moves[move_name][0] < 0 and status_moves[move_name][1] == 'spd' and status_moves[move_name][2] == 'target'):
                    if p.base_stats[3] >= p.base_stats[1]:
                        score += 1
                    for i in get_mon_type(mon):
                        if i not in physical_types:
                            score += 1
                    boost = 0
                    for i in (move1,move2,move3,move4):
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
                    score += min(boost,4.5)
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
                    for i in (move1,move2,move3,move4):
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
                    score += min(boost,4.5)
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
                    for i in (move1,move2,move3,move4):
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
                    score += min(boost,4.5)
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
                    for i in (move1,move2,move3,move4):
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
                    score += min(boost,4.5)

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

        elif move_name in ('GrassWhistle','Hypnosis','Lovely Kiss','Sing','Sleep Powder','Spore','Yawn'):
            score += 2 * 1.8
            if bst <= 350 and (p.base_stats[5] >= 40 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 50):
                score += 1.25
            elif bst <= 435 and (p.base_stats[5] >= 70 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 70):
                score += 1.25
            elif bst <= 530 and (p.base_stats[5] >= 75 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 80):
                score += 1.25
            elif bst > 530 and (p.base_stats[5] >= 80 or ((p.base_stats[0] + p.base_stats[2] + p.base_stats[4])/ 3) >= 90):
                score += 1.25

        elif move_name in ('Glare','Stun Spore','Thunder Wave'):
            score += 2.5 * 1.8
            if bst <= 350 and p.base_stats[5] <= 40:
                score += 1.25
            elif bst <= 435 and p.base_stats[5] <= 70:
                score += 1.25
            elif bst <= 530 and p.base_stats[5] <= 80:
                score += 1.25
            elif bst > 530 and p.base_stats[5] <= 90:
                score += 1.25
        
        elif move_name in ('Confuse Ray','Flatter','Supersonic','Swagger','Sweet Kiss','Teeter Dance'):
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

        elif move_name in ('Recover','Morning Sun','Synthesis','Moonlight'):
            score += 4.5 * 1.8
                    
    elif move_name in ('Cut','Fly','Surf','Strength','Flash','Rock Smash','Waterfall') and learned == True:
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
        for i in (move1,move2,move3,move4):
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
            if get_type_relation(i,move_type) == 0.5:
                score += 0.1
            elif get_type_relation(i,move_type) == 1:
                score += 0.2
            elif get_type_relation(i,move_type) == 2 and ((len(my_mon_type) == 1 and get_type_relation(my_mon_type[0],i) >= 2)
            or (len(my_mon_type) == 2 and get_type_relation(my_mon_type[0],i) * get_type_relation(my_mon_type[1],i) >= 2)):
                score += 0.5
            elif get_type_relation(i,move_type) == 2 and ((len(my_mon_type) == 1 and get_type_relation(i,my_mon_type[0]) <= 1)
            or (len(my_mon_type) == 2 and get_type_relation(i,my_mon_type[0]) <= 1 and get_type_relation(i,my_mon_type[1]) <= 1)):
                score += 0.4
            elif get_type_relation(i,move_type) == 2:
                score += 0.35
        if move_name in ('Bounce','Dig','Dive','Fly','Focus Punch','Razor Wind','Skull Bash','Sky Attack','SolarBeam'):
            score = score * 0.8
        elif move_name in ('Hyper Beam','Frenzy Plant','Blast Burn','Hydro Cannon'):
            score = score * 0.85
        elif move_name in ('Outrage','Petal Dance'):
            score = score * 0.9
        elif move_power < 60:
            score = score ** 0.85
    return score

# print(get_move_score('Slash','Water Spout','Meteor Mash','Earthquake','Tackle','Persian',False))

def learn_move():
    move1_img = ImageGrab.grab(bbox=(1581,163,1890,208))
    move1_name = pyt.image_to_string(move1_img, config='--psm 7')
    move1_name = move1_name.capitalize()
    move1_name = re.sub('[^a-zA-Z-]', '', move1_name)
    move1_name = dfl.get_close_matches(move1_name,Gens1to3_Moves,cutoff=0.1)[0]

    move1_power = df.query(f'Name==\'{move1_name}\'')['Power']
    move1_power = move1_power.to_string(index=False)
    if move1_power == 'NaN':
        move1_power = 0
    else:
        move1_power = int(move1_power)

    move2_img = ImageGrab.grab(bbox=(1581,268,1890,313))
    move2_name = pyt.image_to_string(move2_img, config='--psm 7')
    move2_name = move2_name.capitalize()
    move2_name = re.sub('[^a-zA-Z-]', '', move2_name)
    move2_name = dfl.get_close_matches(move2_name,Gens1to3_Moves,cutoff=0.1)[0]

    move2_power = df.query(f'Name==\'{move2_name}\'')['Power']
    move2_power = move2_power.to_string(index=False)
    if move2_power == 'NaN':
        move2_power = 0
    else:
        move2_power = int(move2_power)
    
    move3_img = ImageGrab.grab(bbox=(1581,373,1890,418))
    move3_name = pyt.image_to_string(move3_img, config='--psm 7')
    move3_name = move3_name.capitalize()
    move3_name = re.sub('[^a-zA-Z-]', '', move3_name)
    move3_name = dfl.get_close_matches(move3_name,Gens1to3_Moves,cutoff=0.1)[0]

    move3_power = df.query(f'Name==\'{move3_name}\'')['Power']
    move3_power = move3_power.to_string(index=False)
    if move3_power == 'NaN':
        move3_power = 0
    else:
        move3_power = int(move3_power)

    move4_img = ImageGrab.grab(bbox=(1581,478,1890,523))
    move4_name = pyt.image_to_string(move4_img, config='--psm 7')
    move4_name = move4_name.capitalize()
    move4_name = re.sub('[^a-zA-Z-]', '', move4_name)
    move4_name = dfl.get_close_matches(move4_name,Gens1to3_Moves,cutoff=0.1)[0]

    move4_power = df.query(f'Name==\'{move4_name}\'')['Power']
    move4_power = move4_power.to_string(index=False)
    if move4_power == 'NaN':
        move4_power = 0
    else:
        move4_power = int(move4_power)

    move5_img = ImageGrab.grab(bbox=(1581,583,1890,628))
    move5_img = cv2.cvtColor(np.array(move5_img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(move5_img, cv2.COLOR_BGR2HSV)
    lower_val = np.array([0,0,0])
    upper_val = np.array([145,145,145])
    mask = cv2.inRange(hsv, lower_val, upper_val)
    pil_image = Image.fromarray(cv2.cvtColor(mask, cv2.COLOR_BGR2RGB))
    move5_name = pyt.image_to_string(pil_image, config='--psm 7')
    move5_name = move5_name.capitalize()
    move5_name = re.sub('[^a-zA-Z-]', '', move5_name)
    move5_name = dfl.get_close_matches(move5_name,Gens1to3_Moves,cutoff=0.1)[0]

    move5_power = df.query(f'Name==\'{move5_name}\'')['Power']
    move5_power = move5_power.to_string(index=False)
    if move5_power == 'NaN':
        move5_power = 0
    else:
        move5_power = int(move5_power)
    # get mon name
    # tiebreaker is pp
    mon_name_img = ImageGrab.grab(bbox=(1122,150,1389,208)).convert('RGB')
    inv_img = ImageOps.invert(mon_name_img)
    inv_img = cv2.cvtColor(np.array(inv_img), cv2.COLOR_RGB2BGR)
    hsv2 = cv2.cvtColor(inv_img, cv2.COLOR_BGR2HSV)
    lower_val2 = np.array([0,0,0]) 
    upper_val2 = np.array([65,175,85])
    mask2 = cv2.inRange(hsv2, lower_val2, upper_val2)
    pil_image2 = Image.fromarray(cv2.cvtColor(mask2, cv2.COLOR_BGR2RGB))
    mon_name = pyt.image_to_string(pil_image2, config='--psm 7')
    mon_name = mon_name.capitalize()

    if (mon_name.find('R. ') == 0 or mon_name.find('r. ') in (1,2)) and ('m' in mon_name or 'n' in mon_name) and 'i' in mon_name and 'e' in mon_name:
        mon_name_readjusted = 'Mr. Mime'
        
    else:
        mon_name_readjusted = re.sub('[^a-zA-Z]', '', mon_name)

    mon_name_readjusted = dfl.get_close_matches(mon_name_readjusted,Gen1_Pokemon,cutoff=0.1)[0]

    print(move1_name,move2_name,move3_name,move4_name,move5_name,mon_name,mon_name_readjusted)

    scores = []

    move1_score = get_move_score(move1_name,move2_name,move3_name,move4_name,move5_name,mon_name_readjusted,True)
    scores.append((1,move1_name,move1_power,move1_score))
    move2_score = get_move_score(move2_name,move1_name,move3_name,move4_name,move5_name,mon_name_readjusted,True)
    scores.append((2,move2_name,move2_power,move2_score))
    move3_score = get_move_score(move3_name,move1_name,move2_name,move4_name,move5_name,mon_name_readjusted,True)
    scores.append((3,move3_name,move3_power,move3_score))
    move4_score = get_move_score(move4_name,move1_name,move2_name,move3_name,move5_name,mon_name_readjusted,True)
    scores.append((4,move4_name,move4_power,move4_score))
    move5_score = get_move_score(move5_name,move1_name,move2_name,move3_name,move4_name,mon_name_readjusted,False)
    
    scores.sort(key = lambda x: x[3])
    
    print(scores)
    print(move5_score)

    if move5_score >= scores[0][3] and scores[0][3] < 2:
        pyd.press('down',scores[0][0] - 1,0.5)
        pyd.press('z')

    elif move5_score < scores[0][3]:
        pyd.press('x')
    
    elif move5_name in ('PoisonPowder','Toxic','Will-O-Wisp','Glare','Stun Spore','Thunder Wave','GrassWhistle',
    'Hypnosis','Lovely Kiss','Sing','Sleep Powder','Spore','Yawn','Confuse Ray','Flatter','Supersonic','Swagger',
    'Sweet Kiss','Teeter Dance','Leech Seed'):
        found_same = False
        removed = False
        for i in scores:
            if i[1] in ('PoisonPowder','Toxic','Will-O-Wisp','Glare','Stun Spore','Thunder Wave','GrassWhistle',
            'Hypnosis','Lovely Kiss','Sing','Sleep Powder','Spore','Yawn','Confuse Ray','Flatter','Supersonic','Swagger',
            'Sweet Kiss','Teeter Dance','Leech Seed'):
                found_same = True
                if move5_score >= i[3]:
                    removed = True
                    pyd.press('down',i[0] - 1,0.5)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down',scores[0][0] - 1,0.5)
                pyd.press('z')
            else:
                pyd.press('x')
        elif removed == False:
            pyd.press('x')
    
    elif move5_power == 0:
        found_same = False
        removed = False
        for i in scores:
            if i[1] not in ('PoisonPowder','Toxic','Will-O-Wisp','Glare','Stun Spore','Thunder Wave','GrassWhistle',
            'Hypnosis','Lovely Kiss','Sing','Sleep Powder','Spore','Yawn','Confuse Ray','Flatter','Supersonic','Swagger',
            'Sweet Kiss','Teeter Dance','Leech Seed') and i[2] == 0:
                found_same = True
                if move5_score >= i[3]:
                    removed = True
                    pyd.press('down',i[0] - 1,0.5)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down',scores[0][0] - 1,0.5)
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
                    pyd.press('down',i[0] - 1,0.5)
                    pyd.press('z')
                    break
        if found_same == False:
            if move5_score >= scores[0][3]:
                pyd.press('down',scores[0][0] - 1,0.5)
                pyd.press('z')
            else:
                pyd.press('x')
        elif removed == False:
            pyd.press('x')

def continue_text(image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_val = np.array([0,100,100])
    upper_val = np.array([10,255,255])
    mask = cv2.inRange(hsv, lower_val, upper_val)
    hasRed = np.sum(mask)
    if hasRed > 0:
        return True
    else:
        return False

# time.sleep(3)
# pyd.press('z')

# while True:
#     move_used_img = ImageGrab.grab(bbox=(1025, 531, 1747, 656))
#     move_used1 = pyt.image_to_string(move_used_img)
#     move_used1 = move_used1.capitalize()
#     if 'make' in move_used1 and 'room' in move_used1:
#         time.sleep(1.5)
#         pyd.press('z')
#         time.sleep(2.5)
#         learn_move()
#         time.sleep(2.5)
#         if continue_text(move_used_img) == False:
#             pyd.press('z')
#     elif continue_text(move_used_img) == True:
#             pyd.press('z')

# import mss
# # mss: 0.23897319078445434
# # PIL: 0.263167507648468
# total = 0
# for i in range(100):
#     start = time.time()
#     # img = ImageGrab.grab((1919,0,1920,1))
#     sct_img = mss.mss().grab((1025,531,1747,656))
#     img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
#     move_used1 = pyt.image_to_string(img)
#     move_used1 = move_used1.capitalize()
#     # rgbimg = img.convert('RGB')
#     # img.getpixel((0,0))
#     # print(rgbimg.getpixel((0,0)))
#     total += time.time() - start
# print(move_used1)
# print(total / 100)
# x = [0,0,0,0,1]
# print(len('it hurt it'))
# count = 0
# img = Image.open(r'C:\Users\arthu\Pictures\Screenshots\Screenshot 2023-09-16 184531.png')
# img = img.crop((1025,531,1747,656))
# move_used1 = pyt.image_to_string(img)
# move_used1 = move_used1.capitalize()
# print('was freed' in move_used1)
# for i in range(500):
#     colorofbox = get_color(1043,515)
#     colorofbox2 = get_color(1043,533)
#     if colorofbox not in ((200,168,72),(198,166,71)):
#         print('1:')
#         print(colorofbox)
#     if colorofbox2 not in ((40,80,104),(40,79,103)):
#         print('2:')
#         print(colorofbox2)
#     if colorofbox in ((200,168,72),(198,166,71)) and colorofbox2 in ((40,80,104),(40,79,103)):
#         count+=1
# print(count)
# move_used1 = 'Geodude used\nprc!'
# move_used1 = move_used1.split('\n')[1]
# print(move_used1[:-1])
# (198, 166, 71)
# (40, 79, 103)
# (200, 168, 72)
# lvl up press z and prev_length <= 3 -> different_text
# print(int(int(5)))
# print(np.array(x))
# print(np.array(np.array(x)))
# print(img.getpixel((0,0)))
# img = np.array(sct_img)
# move_used1 = pyt.image_to_string(img)
# move_used1 = move_used1.capitalize()
# print(time.time() - start)
# print(move_used1)
# start = time.time()
# img = ImageGrab.grab((1025, 531, 1747, 656))
# move_used1 = pyt.image_to_string(img)
# move_used1 = move_used1.capitalize()
# print(time.time() - start)
# print(move_used1)
# cv2.imshow('img', img)
# img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
# img.show()
# cv2.waitKey(0)
# cv2.destroyAllWindows()