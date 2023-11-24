import time
import re
import math
import subprocess
import pandas as pd
import difflib as dfl
import pypokedex as pyp
import pytesseract as pyt
import pydirectinput as pyd
from PIL import Image, ImageGrab
from win32gui import FindWindow, GetWindowRect, MoveWindow

time.sleep(3)

# Sizing for VisualBoyAdvance
hwnd = FindWindow(None,'VisualBoyAdvance')
MoveWindow(hwnd,791,15,736,539,True)

# Image to text idenifier
pyt.pytesseract.tesseract_cmd = r'C:\Users\arthu\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# List of all gen 1 Pokemon names
Gen1_Pokemon = ('Bulbasaur','Ivysaur','Venusaur','Charmander','Charmeleon','Charizard','Squirtle','Wartortle',
           'Blastoise','Caterpie','Metapod','Butterfree','Weedle','Kakuna','Beedrill','Pidgey','Pidgeotto',
           'Pidgeot','Rattata','Raticate','Spearow','Fearow','Ekans','Arbok','Pikachu','Raichu','Sandshrew',
           'Sandslash','Nidoran-F','Nidorina','Nidoqueen','Nidoran-M','Nidorino','Nidoking','Clefairy','Clefable',
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
    'Acid Armor': (2,'def','user'),
    'Sharpen': (1,'atk','user'),
    'Cotton Spore': (-2,'spe','target'),
    'Scary Face': (-2,'spe','target'),
    'Belly Drum': (6,'atk','user'),
    'Icy Wind': (-1,'spe','target'),
    'Charm': (-2,'atk','target'),
    'Swagger': (2,'atk','target'),
    'Stockpile': (1,'def',1,'spd','user'),
    'Flatter': (1,'spa','target'),
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

physical_types = ['Normal','Fighting','Poison','Ground','Flying','Bug','Rock','Ghost','Steel',]

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
            time.sleep(0.5)
            pyd.press('left')
        
    elif which_move == 2:
        battle_move = 2
        if prev_move in (0,1):
            pyd.press('right')
        elif prev_move == 3:
            pyd.press('up')
            time.sleep(0.5)
            pyd.press('right')
        elif prev_move == 4:
            pyd.press('up')
            
    elif which_move == 3:
        battle_move = 3
        if prev_move in (0,1):
            pyd.press('down')
        elif prev_move == 2:
            pyd.press('down')
            time.sleep(0.5)
            pyd.press('left')
        elif prev_move == 4:
            pyd.press('left')

    elif which_move == 4:
        battle_move = 4
        if prev_move in (0,1):
            pyd.press('down')
            time.sleep(0.5)
            pyd.press('right')
        elif prev_move == 2:
            pyd.press('down')
        elif prev_move == 3:
            pyd.press('right')
    
    prev_move = battle_move

# Set which_Pokemon to 'plyr' to get name of Player's Pokemon. Any other value gets opposing Pokemon's name. 
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

    mon_lvl = re.sub('[^\d]', '', mon_lvl)

    if len(mon_lvl) > 2 and '00' not in mon_lvl:
        mon_lvl = mon_lvl[1:]

    if mon_lvl == '':
        return 'empty'
    else:
        return mon_lvl

# print(get_pokemon_level('plyr'))

def get_color(x,y):
    img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    rgbimg = img.convert('RGB')
    return rgbimg.getpixel((0,0))

def get_pokemon_HP(which_Pokemon):
    if which_Pokemon == 'plyr':
        x,y = 1829,433
        limit = 1654
    
    else:
        x,y = 1371,212
        limit = 1196

    while x >= limit:
        color = get_color(x,y)
        if (color not in ((97,118,104),(87,108,87),(82,105,89),(80,104,88),(80,103,88),(81,104,88),(81,105,89),(79,71,94),(73,65,89))) or (x == limit + 1):
            # returns a percent that is an integer without the percent sign e.g. return value of 3 = 3%
            return math.ceil(((x - limit)/175) * 100)

        x -= 2

# print(get_pokemon_HP('plyr'))

# Gets HP of a single party member
def get_party_HP(x,y,limit):
    while x >= limit:
        color = get_color(x,y)
        if (color not in ((112,112,112),(126,126,126))) or (x == limit + 1):
            # returns a percent that is an integer without the percent sign e.g. return value of 3 = 3%
            return math.ceil(((x - limit)/175) * 100)
        x -= 2

def get_party_status():
    party = []
    x = 1867
    limit = 1692
    if (get_color(1867,135) == (56,144,216)):
        # slot number refers to position in party with slot 1 being the lead Pokemon
        y = 156
        slot2 = ('slot2',get_pokemon_name('slot2'),get_party_HP(x,y,limit))
        party.append(slot2)
        
    if (get_color(1867,225) == (56,144,216)):
        y = 246
        slot3 = ('slot3',get_pokemon_name('slot3'),get_party_HP(x,y,limit))
        party.append(slot3)

    if (get_color(1867,315) == (56,144,216)):
        y = 336
        slot4 = ('slot4',get_pokemon_name('slot4'),get_party_HP(x,y,limit))
        party.append(slot4)
            
    if (get_color(1867,405) == (56,144,216)):
        y = 426
        slot5 = ('slot5',get_pokemon_name('slot5'),get_party_HP(x,y,limit))
        party.append(slot5)

    if (get_color(1867,495) == (56,144,216)):
        y = 516
        slot6 = ('slot6',get_pokemon_name('slot6'),get_party_HP(x,y,limit))
        party.append(slot6)
    
    return party

# for obj in get_party_status():
#     print(obj)

# Set which_move to an integer --> 1 = top left move, 2 = top right move, 3 = bottom left move, int >= 4 = bottom right move
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

# print(get_pokemon_move(2))

def get_moveset(mon_name,lvl):
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
# foe and soundproof and blocks
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
                if move_used.find('Foe') != 0 and (('paralyzed' in move_used and 'it can’t move' in move_used) or 
                ('is fast' in move_used and 'asleep' in move_used) or ('frozen solid' in move_used) or ('used' in move_used)):
                    my_move_went = False
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
                elif move_used.find('Foe') != 0 and (search_for in move_used and search_again in move_used):
                    my_move_went = True
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
            if check_status_move:
                if move_used.find('Foe') != 0 and (('paralyzed' in move_used and 'it can’t move' in move_used) or 
                ('is fast' in move_used and 'asleep' in move_used) or ('frozen solid' in move_used)):
                    my_move_went = False
                    my_mon_attack = True
                    if opp_mon_attack == False:
                        return None, my_move_went
                elif move_used.find('Foe') != 0 and 'used' in move_used:
                    my_mon_attack = True
                    start3 = time.time()
                    while elapsed3 < 8:
                        status_move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                        status_move_missed = pyt.image_to_string(status_move_missed_img)
                        status_move_missed = status_move_missed.capitalize()
                        
                        if (status_move_missed.find('Foe') != 0 and ('attack' in status_move_missed or 'missed' in status_move_missed)) or \
                        (status_move_missed.find('Foe') == 0 and ('evaded' in status_move_missed)) or \
                        'failed' in status_move_missed or (status_move_missed.find('Foe') == 0 and 'soundproof' in status_move_missed and 'blocks' in status_move_missed):
                            my_move_went = False
                            break

                        elif 'fell' in status_move_missed or 'rose' in status_move_missed:
                            my_move_went = True
                            break

                        elasped3 = time.time() - start3

                    if opp_mon_attack == False:
                        return None, my_move_went
                        
            if 'fainted' in move_used or 'potion' in move_used or 'full restore' in move_used or (move_used.find('Foe') == 0 
                and (('paralyzed' in move_used and 'it can’t move' in move_used) or ('is fast' in move_used and 'asleep' in move_used)
                or ('frozen solid' in move_used))):
                opp_mon_attack = False
                if check_my_move == False and check_status_move == False:
                    return None
                elif my_mon_attack == True:
                    return None, my_move_went
            elif move_used.find('Foe') == 0 and 'used' in move_used and '!' in move_used:
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
                    
                    if move_missed.find('Foe') != 0 and 'used' in move_missed and '!' in move_missed:
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
                    
                    elif (move_missed.find('Foe') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or \
                        (move_missed.find('Foe') != 0 and ('evaded' in move_missed)) or \
                        'failed' in move_missed:
                        hit = False
                        if check_my_move == False:
                            return when_used, move_used, hit
                        elif my_mon_attack == True:
                            return when_used, move_used, hit, my_move_went
                    
                    elif move_missed.find('Foe') != 0 and 'disabled' in move_missed and 'no more!' in move_missed:
                        return when_used, move_used, hit, 'disable off'

                    elif 'reflect' in move_missed and 'wore off' in move_missed:
                        return when_used, move_used, hit, 'reflect off'
                    
                    elif 'light screen' in move_missed and 'wore off' in move_missed:
                        return when_used, move_used, hit, 'lightscreen off'
                    
                    if check_my_move == True and my_mon_attack == False:
                        if move_missed.find('Foe') != 0 and (('paralyzed' in move_missed and 'it can’t move' in move_missed) 
                        or ('is fast' in move_missed and 'asleep' in move_missed) or ('used' in move_missed) or ('frozen solid' in move_missed)
                        or 'fainted' in move_missed):
                            my_move_went = False
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                        elif move_missed.find('Foe') != 0 and (search_for in move_missed and search_again in move_missed):
                            my_move_went = True
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                    
                    if check_status_move == True and my_mon_attack == False:
                        if move_missed.find('Foe') != 0 and (('paralyzed' in move_missed and 'it can’t move' in move_missed) or 
                        ('is fast' in move_missed and 'asleep' in move_missed) or ('frozen solid' in move_missed) or 'fainted' in move_missed):
                            my_move_went = False
                            my_mon_attack = True
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went
                        elif move_missed.find('Foe') != 0 and 'used' in move_missed:
                            my_mon_attack = True
                            start3 = time.time()
                            while elapsed3 < 8:
                                status_move_missed_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
                                status_move_missed = pyt.image_to_string(status_move_missed_img)
                                status_move_missed = status_move_missed.capitalize()
                                
                                if (status_move_missed.find('Foe') != 0 and ('attack' in status_move_missed or 'missed' in status_move_missed)) or \
                                (status_move_missed.find('Foe') == 0 and ('evaded' in status_move_missed)) or \
                                'failed' in status_move_missed or (status_move_missed.find('Foe') == 0 and 'soundproof' in status_move_missed and 'blocks' in status_move_missed):
                                    my_move_went = False
                                    break

                                elif 'fell' in status_move_missed or 'rose' in status_move_missed:
                                    my_move_went = True
                                    break

                                elasped3 = time.time() - start3
                                
                            if disable_check == True:
                                return when_used, move_used, hit, move_disabled, my_move_went
                            return when_used, move_used, hit, my_move_went

                    elapsed2 = time.time() - start2
                    
                if check_my_move or check_status_move:
                    return when_used, move_used, hit, my_move_went
                else:
                    return when_used, move_used, hit

        elapsed = time.time() - start

# print(get_move_used())

def get_move_used2(starting):
    start = starting
    elapsed = 0
    hit = True
    disable_off = False

    move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
    move_used = pyt.image_to_string(move_used_img)
    move_used = move_used.capitalize()
    
    if get_color(1297,618) == (248,0,0):
        pyd.press('z')
        
    elif move_used.find('Foe') != 0 and 'disabled' in move_used and 'no more!' in move_used:
        disable_off = True
    
    elif 'reflect' in move_used and 'wore off' in move_used:
        reflect_off = True

    elif 'light screen' in move_used and 'wore off' in move_used:
        lightscreen_off = True

    elif 'fainted' in move_used or 'potion' in move_used or 'full restore' in move_used or (move_used.find('Foe') == 0 
        and (('paralyzed' in move_used and 'it can’t move' in move_used) or ('is fast' in move_used and 'asleep' in move_used) 
        or ('frozen solid' in move_used))):
        return None, disable_off, reflect_off, lightscreen_off
    elif move_used.find('Foe') == 0 and 'used' in move_used and '!' in move_used:
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
            
            if move_missed.find('Foe') != 0 and 'disabled' in move_missed and 'no more!' in move_missed:
                disable_off = True
            
            elif 'reflect' in move_missed and 'wore off' in move_missed:
                reflect_off = True

            elif 'light screen' in move_missed and 'wore off' in move_missed:
                lightscreen_off = True

            elif move_missed.find('Foe') != 0 and 'used' in move_missed and '!' in move_missed:
                return when_used, move_used, hit, disable_off, reflect_off, lightscreen_off
            
            elif move_used == 'Disable' and 'disabled' in move_missed and '!' in move_missed:
                move_disabled = move_missed.split('\n')[0]
                move_disabled = ' '.join(move_disabled.split()[1:])
                move_disabled = dfl.get_close_matches(move_disabled,Gens1to3_Moves,cutoff=0.1)[0]
                # (0.7670919895172119, 'Disable', True, 2.7191858291625977, 'Tackle')
                return when_used, move_used, hit, move_disabled, disable_off, reflect_off, lightscreen_off
            
            elif ((move_missed.find('Foe') == 0 and ('attack' in move_missed or 'missed' in move_missed)) or 
                (move_missed.find('Foe') != 0 and ('evaded' in move_missed)) or 
                'failed' in move_missed) and '!' in move_missed:
                hit = False
                return when_used, move_used, hit, disable_off, reflect_off, lightscreen_off
            
            elapsed = time.time() - start2
        return when_used, move_used, hit, disable_off, reflect_off, lightscreen_off
    return ''

def get_move_type(move_name):
    get_move_type = df.query(f'Name==\'{move_name}\'')['Type']
    return get_move_type.to_string(index=False)

def get_mon_type(mon_name):
    mon_type = df2.query(f'Name==\'{mon_name}\'')['Type']
    return mon_type.to_string(index=False).split(' ')

def get_type_relation(typing1,typing2):
    type_relation = df3.query(f'Type==\'{typing1}\'')[typing2]
    return float(type_relation.to_string(index=False))

# atk_mon = attacking Pokemon, def_mon = defending Pokemon
# atk_lvl and def_lvl have to be integers in string form e.g. '50'
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

# print(calc_move('Gengar','Chansey',str(50),str(50),'Fire Punch'))

start = time.time()
elapsed = 0
battle = False

while elapsed < 120:
    battle_start_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
    battle_start = pyt.image_to_string(battle_start_img)
    battle_start = battle_start.capitalize()
    if 'would like to battle!' in battle_start and get_color(1043,515) == (200,168,72) and get_color(1043,533) == (40,80,104):
        for i in range(5):
            which_trainer_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656))
            which_trainer = pyt.image_to_string(which_trainer_img)
            which_trainer = which_trainer.capitalize()
            if 'Elite' in which_trainer or 'Champion' in which_trainer:
                opp_ivs = '31'
                break
            else:
                opp_ivs = '12'
        battle = True
        pyd.press('z')
        break

    elapsed = time.time() - start

my_mon_struggle = False
prev_opp_faint = False
make_move = False
new_my_mon = True
new_opp_mon = True
switch_mon = False
make_switch = False
no_switch = False
fight = False
my_mon_used_move = False
my_mon_faint = False

while battle:
    if get_color(1491,516) == (208,160,208) and make_switch == False:
        make_move = True

        if new_my_mon == True and switch_mon == False:
            my_mon = get_pokemon_name('plyr')
            my_mon_lvl = get_pokemon_level('plyr')
            my_stat_stages = [0,0,0,0,0]
            my_mon_used_move = False
            check_status_move = False
            used_status_move = False
            prev_move = 0
            disabled_move = ''
            make_switch = False
            my_mon_faint = False

            if my_mon == 'Gyarados':
                opp_stat_stages[0] -= 1
                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)

        if new_opp_mon == True:    
            opp_mon = get_pokemon_name('opp')
            opp_mon_lvl = get_pokemon_level('opp')
            opp_stat_stages = [0,0,0,0,0]
            actual_moves = []
            prev_list_length = 0
            check_status_move = False

            if opp_mon == 'Gyarados':
                my_stat_stages[0] -= 1
                my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)

        if my_mon_lvl == 'empty' or opp_mon_lvl == 'empty':
            if my_mon_lvl == 'empty' and opp_mon_lvl != 'empty':
                my_mon_lvl = opp_mon_lvl
            elif my_mon_lvl != 'empty' and opp_mon_lvl == 'empty':
                opp_mon_lvl = my_mon_lvl
            elif my_mon_lvl == 'empty' and opp_mon_lvl == 'empty':
                my_mon_lvl = '30'
                opp_mon_lvl = '30'
        
        if new_opp_mon == True:
            opp_moves = get_moveset(opp_mon,int(opp_mon_lvl))

        opp_HP = get_pokemon_HP('opp')

        opp_dmgs = []
        for i in range(len(opp_moves)):
            opp_dmgs.append((opp_moves[i],calc_move_max(opp_mon,opp_mon_lvl,opp_ivs,opp_stat_stages,my_mon,my_mon_lvl,'31',my_stat_stages,str(opp_HP),opp_moves[i])[0]))
        
        opp_dmgs.sort(key = lambda x: x[1], reverse = True)

        opp_move_name = opp_dmgs[0][0]
        opp_move_name = dfl.get_close_matches(opp_move_name,Gens1to3_Moves,cutoff=0.1)[0]

        opp_move_dmg = opp_dmgs[0][1]

        calc_info = calc_move_max(opp_mon,opp_mon_lvl,opp_ivs,opp_stat_stages,my_mon,my_mon_lvl,'31',my_stat_stages,str(opp_HP),opp_moves[0])
        
        if len(actual_moves) > prev_list_length:
            opp_actual_moves_dmgs = []
            for i in range(len(actual_moves)):
                opp_actual_moves_dmgs.append((actual_moves[i],calc_move_max(opp_mon,opp_mon_lvl,opp_ivs,opp_stat_stages,my_mon,my_mon_lvl,'31',my_stat_stages,str(opp_HP),actual_moves[i])[0]))
            
            opp_actual_moves_dmgs.sort(key = lambda x: x[1], reverse = True)

            opp_actual_move_dmg = opp_actual_moves_dmgs[0][1]

            if opp_actual_move_dmg > opp_move_dmg or len(actual_moves) == 4:
                opp_move_name = opp_actual_moves_dmgs[0][0]
                opp_move_dmg = opp_actual_move_dmg

        my_HP = get_pokemon_HP('plyr')

        if my_mon_struggle == True and no_switch == False:
            new_opp_mon = False
            make_switch = True

        if no_switch:
            pyd.press('z')
            fight = True
            time.sleep(1.5)
            no_moves_img = ImageGrab.grab(bbox=(1029, 531, 1538, 656))
            no_moves = pyt.image_to_string(no_moves_img)
            no_moves = no_moves.capitalize()
                
            if no_moves.find('Foe') != 0 and 'moves left!' in no_moves:
                my_mon_struggle = True
            else:
                for i in range(len(usable_moves)):
                    move_to_use = usable_moves[i]
                    select_move(move_to_use[0])
                    time.sleep(0.5)
                    if get_color(1631,568) == (232,1,1) or move_to_use[1] == disabled_move:
                        pass
                    else:
                        break

            my_mon_used_move = True
            pyd.press('z')

        # Switch when my mon is in crit range and the opposing mon outspeeds
        elif make_switch == False and opp_move_dmg/my_HP >= 0.5 and calc_info[1] >= calc_info[2]:
            make_switch = True
            fight = False

        # If opp KOs but my mon outspeeds check whether my mon KOs
        elif make_switch == False:
            pyd.press('z')
            fight = True
            
            time.sleep(1.5)
            no_moves_img = ImageGrab.grab(bbox=(1029, 531, 1538, 656))
            no_moves = pyt.image_to_string(no_moves_img)
            no_moves = no_moves.capitalize()
                
            if no_moves.find('Foe') != 0 and 'moves left!' in no_moves:
                my_mon_struggle = True
                my_mon_used_move = True
                pyd.press('z')

            else:
                my_moves = []
                for i in range(1,5):
                    move = get_pokemon_move(i)
                    if move != 'empty':
                        my_moves.append(move)
                    
                if len(my_moves) == 0:
                    make_switch = True

                if make_switch == False:
                    usable_moves = []
                    for i in range(len(my_moves)):
                        usable_moves.append((my_moves[i][0],my_moves[i][1],calc_move(my_mon,my_mon_lvl,'31',my_stat_stages,opp_mon,opp_mon_lvl,opp_ivs,opp_stat_stages,str(my_HP),my_moves[i][1])[0]))
                        
                    usable_moves.sort(key = lambda x: x[2], reverse = True)
                print(usable_moves)
                print(my_moves)
                print(my_mon_lvl)
                print(opp_mon_lvl)
                # Get strongest move that does damage and has pp
                if make_switch == False:
                    for i in range(len(usable_moves)):
                        move_to_use = usable_moves[i]
                        my_move_name = move_to_use[1]
                        select_move(move_to_use[0])
                        time.sleep(1)
                        if move_to_use[2] == 0:
                            make_switch = True
                            break
                        elif get_color(1631,568) == (232,1,1) or move_to_use[1] == disabled_move:
                            print(my_move_name + ' is not usable')
                            pass
                        elif my_move_name in ('Recover','Moonlight') and my_HP <= 50 and opp_move_dmg < 50:
                            break
                        else:
                            break
                    print(move_to_use)
                # Get status moves
                if make_switch == False and my_move_name not in ('Recover','Moonlight') and check_status_move == False and opp_move_dmg/my_HP < (1/3) and int(opp_mon_lvl) >= int(my_mon_lvl):
                    print('checking status moves')
                    potential_status_moves = []
                    for i in range(len(usable_moves)):
                        move_to_use2 = usable_moves[i]
                        select_move(move_to_use2[0])
                        time.sleep(1)
                        if get_color(1631,568) == (232,1,1) or move_to_use2[1] == disabled_move:
                            pass
                        elif move_to_use2[2] == 0 and move_to_use2[1] in status_moves:
                            potential_status_moves.append((move_to_use2[0],move_to_use2[1]))
                    
                    if len(potential_status_moves) > 0:
                        usable_status_moves = []
                        for i in potential_status_moves:
                            if len(status_moves[i[1]]) == 3:
                                if ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][2] == 'target') or
                                (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][2] == 'user')) and \
                                get_move_type(opp_move_name) in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1]))
                                
                                elif ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][2] == 'target') or
                                (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][2] == 'user')) and \
                                get_move_type(opp_move_name) not in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1]))

                                elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][2] == 'user') or
                                (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][2] == 'target')) and \
                                get_move_type(my_move_name) in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1]))
                                
                                elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][2] == 'user') or
                                (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][2] == 'target')) and \
                                get_move_type(my_move_name) not in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1]))

                                elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spe' and status_moves[i[1]][2] == 'user') or
                                (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spe' and status_moves[i[1]][2] == 'target')) and calc_info[1] >= calc_info[2]:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1]))
                                    
                            else:
                                if ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][4] == 'target') or
                                (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][4] == 'user')) and \
                                get_move_type(opp_move_name) in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1],status_moves[i[1]][2],status_moves[i[1]][3]))
                                
                                elif ((status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][4] == 'target') or
                                (status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][4] == 'user')) and \
                                get_move_type(opp_move_name) not in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1],status_moves[i[1]][2],status_moves[i[1]][3]))

                                elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'atk' and status_moves[i[1]][4] == 'user') or
                                (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'def' and status_moves[i[1]][4] == 'target')) and \
                                get_move_type(my_move_name) in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1],status_moves[i[1]][2],status_moves[i[1]][3]))
                                
                                elif ((status_moves[i[1]][0] > 0 and status_moves[i[1]][1] == 'spa' and status_moves[i[1]][4] == 'user') or
                                (status_moves[i[1]][0] < 0 and status_moves[i[1]][1] == 'spd' and status_moves[i[1]][4] == 'target')) and \
                                get_move_type(my_move_name) not in physical_types:
                                    usable_status_moves.append((i[0],i[1],status_moves[i[1]][0],status_moves[i[1]][1],status_moves[i[1]][2],status_moves[i[1]][2]))

                        if len(usable_status_moves) > 0:
                            usable_status_moves.sort(key = lambda x: (len(x),abs(x[2])), reverse = True)
                            used_status_move = True
                            status_move_name = usable_status_moves[0][1]
                            select_move(usable_status_moves[0][0])
                        
                        else:
                            select_move(move_to_use[0])
                            time.sleep(0.5)
    
                    else:
                        select_move(move_to_use[0])
                        time.sleep(0.5)
    
                    check_status_move = True
                        
                # get status move with the largest decrease or increase based on the opponents move or my move
                
                if make_switch == False and ((move_to_use[2]/get_pokemon_HP('opp') >= 1 and calc_info[1] < calc_info[2]) or (opp_move_dmg/my_HP <= 0.5)):
                    print('attack')
                    pyd.press('z')
                    my_mon_used_move = True
                    switch_mon = False
                
                else:
                    make_switch = True

    if make_switch == True and no_switch == False:
        if get_color(1491,516) == (208,160,208):
            if fight == False:
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('z')
            else:
                pyd.press('x')
                time.sleep(0.5)
                pyd.press('down')
                time.sleep(0.5)
                pyd.press('z')
            
        time.sleep(2.5)
        
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
                    def_type_relations.append(get_type_relation(t,move_type))
                    for j in get_mon_type(opp_mon):
                        off_type_relations.append(get_type_relation(j,t))
                print(def_type_relations)
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

            updated_party.sort(key = lambda x: (x[3],-(x[4]),-(x[5]),-(x[2])))
            print(updated_party)
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
            switch_after_faint = True
            pyd.press('down',int(send_out[-1]) - 1,0.5)
            pyd.press('z')
            time.sleep(0.5)
            pyd.press('z')
            make_move = True
            time.sleep(2)

        elif no_switch == False:
            my_mon_struggle = False
            new_my_mon = True
            switch_mon = True
            pyd.press('down',int(send_out[-1]) - 1,0.5)
            pyd.press('z')
            time.sleep(0.5)
            pyd.press('z')
            make_move = True

        else:
            pyd.press('x')
            time.sleep(2)
            pyd.press('up')
            make_move = False

        if my_mon_faint == False:
            make_switch = False

        fight = False

    #check if pokemon is still fighting
    if make_move == True:
        if make_switch == False and my_move_name in ('Bounce','Dig','Dive','Fly','Razor Wind','Skull Bash','Sky Attack','SolarBeam') and used_status_move == False:
            check_my_move = True
        else:
            check_my_move = False
        
        if switch_after_faint == True:
            opp_move_used = None
        elif used_status_move == True:
            opp_move_used = get_move_used(check_my_move,used_status_move,status_move_name,disabled_move)
        else:
            opp_move_used = get_move_used(check_my_move,used_status_move,my_move_name,disabled_move)
        
        if (opp_move_used != None and opp_move_used[0] != None) and opp_move_used[1] not in actual_moves:
            prev_list_length = len(actual_moves)
            actual_moves.append(opp_move_used[1])
        
        if disabled_move != '':
            if len(opp_move_used) == 4 and opp_move_used[3] == 'disable off':
                disabled_move == ''

        keep_checking = True
        opp_move_used2 = ''

        # disabled red arrow
        while get_color(1491,516) != (208,160,208) and get_color(1098,201) == (248,248,216) and get_color(1525,431) == (248,248,216):
            if check_my_move == True and keep_checking == True and ((len(opp_move_used) == 2 and opp_move_used[1] == True) or (len(opp_move_used) == 4 and
                opp_move_used[3] == True) or (len(opp_move_used) == 5 and opp_move_used[4] == True)):
                starting = time.time()
                while opp_move_used2 == '':
                    opp_move_used2 = get_move_used2(starting,disabled_move)
                keep_checking = False

                if (opp_move_used2 != None and opp_move_used2[0] != None) and opp_move_used2[1] not in actual_moves:
                    prev_list_length = len(actual_moves)
                    actual_moves.append(opp_move_used2[1])
                    
                if disabled_move != '':
                    if len(opp_move_used2) == 2:
                        if opp_move_used2[1] == True:
                            disabled_move = ''

                    elif len(opp_move_used2) == 4:
                        if opp_move_used2[3] == True:
                            disabled_move = ''
                    
                    elif len(opp_move_used2) == 5:
                        if opp_move_used2[4] == True:
                            disabled_move = ''

            if disabled_move != '':
                move_used_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656)) # change size of box check for disable in case it happens after initiating a two turn move
                move_used = pyt.image_to_string(move_used_img)
                move_used = move_used.capitalize()
                
                if move_used.find('Foe') != 0 and 'disabled' in move_used and 'no more!' in move_used:
                    disabled_move == ''
            
            if get_color(1297,618) == (248,0,0) and (opp_move_used != None and opp_move_used[0] != None) and opp_move_used[1] == 'Disable':
                pyd.press('z')

        if used_status_move == True:
            if (len(opp_move_used) == 2 and opp_move_used[1] == True) or (len(opp_move_used) == 4 and
                opp_move_used[3] == True) or (len(opp_move_used) == 5 and opp_move_used[4] == True):
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
                else:
                    if status_moves[usable_status_moves[0][1]][4] == 'user':
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
                check_status_move = False

        used_status_move = False

        if get_color(1098,201) == (248,248,216):
            new_opp_mon = False
            prev_opp_faint = False
        
        else:
            # check if battle is done
            new_opp_mon = True
            no_switch = False
            prev_opp_faint = True
            pyd.press('z')
            
            break_loop = False

            while get_color(1043,515) == (200,168,72) and get_color(1043,533) == (40,80,104) and get_color(1491,516) != (208,160,208):
                for i in range(10):
                    after_moves_img = ImageGrab.grab(bbox=(1029, 531, 1747, 656)) # change size of box
                    after_moves = pyt.image_to_string(after_moves_img)
                    after_moves = after_moves.capitalize()
                
                    if 'Player' in after_moves and 'defeated' in after_moves:
                        print('battle over')
                        while get_color(1043,515) == (200,168,72) and get_color(1043,533) == (40,80,104):
                            pyd.press('z')
                        exit()
                    elif after_moves.find('Foe') != 0 and 'disabled' in after_moves:
                        disabled_move == ''

                    elif 'make' in after_moves and 'room' in after_moves:

                    elif get_color(1525,431) != (248,248,216) or get_color(1098,201) == (248,248,216):
                        break_loop = True
                        break
                
                    time.sleep(0.25)

                if break_loop == True:
                    break
                
                x = 1180
                while x <= 1468:
                    if get_color(x,618) == (248,0,0):
                        pyd.press('z')
                        break
                    x += 2
                # disable wears off exactly after opp mon faints and after pressing A and before sending out new mon
            # opp mon faints after switching in my mon
        forced_switch = False
        
        if get_color(1525,431) == (248,248,216):
            # check status
            if (opp_move_used != None and opp_move_used[0] != None) and opp_move_used[1] in ('Whirlwind','Roar') and opp_move_used[2] == True:
                switch_mon = True
                forced_switch = True
                my_mon_struggle = False

            elif (opp_move_used != None and opp_move_used[0] != None) and opp_move_used[1] == 'Disable':
                if (opp_move_used[0] < 2 and new_my_mon == True) or opp_move_used[2] == False:
                    pass
                else:
                    disabled_move = opp_move_used[3]
            
            if check_my_move == True:
                if (opp_move_used2 != None and opp_move_used2[0] != None) and opp_move_used2[1] in ('Whirlwind','Roar') and opp_move_used2[2] == True:
                    switch_mon = True
                    forced_switch = True
                    my_mon_struggle = False

                elif (opp_move_used2 != None and opp_move_used2[0] != None) and opp_move_used2[1] == 'Disable':
                    if (opp_move_used2[0] < 2.5 and new_my_mon == True) or opp_move_used2[2] == False:
                        pass
                    else:
                        disabled_move = opp_move_used2[3]

            if switch_mon == True:
                print('getting new mon')
                my_mon = get_pokemon_name('plyr')
                my_mon_lvl = get_pokemon_level('plyr')
                my_stat_stages = [0,0,0,0,0]
                my_mon_used_move = False
                check_status_move = False
                prev_move = 0
                disabled_move = ''
                make_switch = False
                my_mon_faint = False
                print(my_mon_lvl)
                if my_mon == 'Gyarados':
                    opp_stat_stages[0] -= 1
                    opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                
            if (opp_move_used != None and opp_move_used[0] != None) and forced_switch == False and opp_move_used[1] in status_moves and opp_move_used[2] == True:
                if len(status_moves[opp_move_used[1]]) == 3:
                    if status_moves[opp_move_used[1]][2] == 'user':
                        if status_moves[opp_move_used[1]][1] == 'atk':
                            opp_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'def':
                            opp_stat_stages[1] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spa':
                            opp_stat_stages[2] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spd':
                            opp_stat_stages[3] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spe':
                            opp_stat_stages[4] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
                    else:
                        if status_moves[opp_move_used[1]][1] == 'atk':
                            my_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'def':
                            my_stat_stages[1] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spa':
                            my_stat_stages[2] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spd':
                            my_stat_stages[3] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spe':
                            my_stat_stages[4] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
                else:
                    if status_moves[opp_move_used[1]][4] == 'user':
                        if status_moves[opp_move_used[1]][1] == 'atk' and status_moves[opp_move_used[1]][3] == 'def':
                            opp_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                            opp_stat_stages[1] += status_moves[opp_move_used[1]][2]
                            opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'atk' and status_moves[opp_move_used[1]][3] == 'spe':
                            opp_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                            opp_stat_stages[4] += status_moves[opp_move_used[1]][2]
                            opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spa' and status_moves[opp_move_used[1]][3] == 'spd':
                            opp_stat_stages[2] += status_moves[opp_move_used[1]][0]
                            opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                            opp_stat_stages[3] += status_moves[opp_move_used[1]][2]
                            opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                    else:
                        if status_moves[opp_move_used[1]][1] == 'atk' and status_moves[opp_move_used[1]][3] == 'def':
                            my_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                            my_stat_stages[1] += status_moves[opp_move_used[1]][2]
                            my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'atk' and status_moves[opp_move_used[1]][3] == 'spe':
                            my_stat_stages[0] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                            my_stat_stages[4] += status_moves[opp_move_used[1]][2]
                            my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                        elif status_moves[opp_move_used[1]][1] == 'spa' and status_moves[opp_move_used[1]][3] == 'spd':
                            my_stat_stages[2] += status_moves[opp_move_used[1]][0]
                            my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                            my_stat_stages[3] += status_moves[opp_move_used[1]][2]
                            my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                
            if check_my_move == True:
                if (opp_move_used2 != None and opp_move_used2[0] != None) and opp_move_used2[1] in status_moves and opp_move_used2[2] == True:
                    if len(status_moves[opp_move_used2[1]]) == 3:
                        if status_moves[opp_move_used2[1]][2] == 'user':
                            if status_moves[opp_move_used2[1]][1] == 'atk':
                                opp_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                            elif status_moves[opp_move_used[1]][1] == 'def':
                                opp_stat_stages[1] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used[1]][1] == 'spa':
                                opp_stat_stages[2] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                            elif status_moves[opp_move_used[1]][1] == 'spd':
                                opp_stat_stages[3] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                            elif status_moves[opp_move_used[1]][1] == 'spe':
                                opp_stat_stages[4] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[4] = max(min(opp_stat_stages[4], 6), -6)
                        else:
                            if status_moves[opp_move_used2[1]][1] == 'atk':
                                my_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'def':
                                my_stat_stages[1] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'spa':
                                my_stat_stages[2] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'spd':
                                my_stat_stages[3] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'spe':
                                my_stat_stages[4] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[4] = max(min(my_stat_stages[4], 6), -6)
                    else:
                        if status_moves[opp_move_used2[1]][4] == 'user':
                            if status_moves[opp_move_used2[1]][1] == 'atk' and status_moves[opp_move_used2[1]][3] == 'def':
                                opp_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                                opp_stat_stages[1] += status_moves[opp_move_used2[1]][2]
                                opp_stat_stages[1] = max(min(opp_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'atk' and status_moves[opp_move_used2[1]][3] == 'spe':
                                opp_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[0] = max(min(opp_stat_stages[0], 6), -6)
                                opp_stat_stages[4] += status_moves[opp_move_used2[1]][2]
                                opp_stat_stages[4] = max(min(opp_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'spa' and status_moves[opp_move_used2[1]][3] == 'spd':
                                opp_stat_stages[2] += status_moves[opp_move_used2[1]][0]
                                opp_stat_stages[2] = max(min(opp_stat_stages[2], 6), -6)
                                opp_stat_stages[3] += status_moves[opp_move_used2[1]][2]
                                opp_stat_stages[3] = max(min(opp_stat_stages[3], 6), -6)
                        else:
                            if status_moves[opp_move_used2[1]][1] == 'atk' and status_moves[opp_move_used2[1]][3] == 'def':
                                my_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                                my_stat_stages[1] += status_moves[opp_move_used2[1]][2]
                                my_stat_stages[1] = max(min(my_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'atk' and status_moves[opp_move_used2[1]][3] == 'spe':
                                my_stat_stages[0] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[0] = max(min(my_stat_stages[0], 6), -6)
                                my_stat_stages[4] += status_moves[opp_move_used2[1]][2]
                                my_stat_stages[4] = max(min(my_stat_stages[1], 6), -6)
                            elif status_moves[opp_move_used2[1]][1] == 'spa' and status_moves[opp_move_used2[1]][3] == 'spd':
                                my_stat_stages[2] += status_moves[opp_move_used2[1]][0]
                                my_stat_stages[2] = max(min(my_stat_stages[2], 6), -6)
                                my_stat_stages[3] += status_moves[opp_move_used2[1]][2]
                                my_stat_stages[3] = max(min(my_stat_stages[3], 6), -6)

            if my_mon_used_move:
                new_my_mon = False

                # switch in
                # disable fails b/c switch mon = True -> new mon = True
                # disable moves first
                # disable fails b/c less than 2 seconds and new mon = True
                # my mon attacks second (used move = True -> new mon = False)
                # disable first
                # disable hits (works when new_my_mon == False)
            
            if my_mon_struggle == True and prev_opp_faint == False:
                make_switch = True
            else:
                make_switch = False

        else:
            my_mon_faint = True
            new_my_mon = True
            make_switch = True
            switch_mon = False
            no_switch = False
            my_mon_struggle = False

            while get_color(1043,515) == (200,168,72) and get_color(1043,533) == (40,80,104):
                for i in range(10):
                    battle_over_img = ImageGrab.grab(bbox=(1029, 531, 1611, 656))
                    battle_over = pyt.image_to_string(battle_over_img)
                    battle_over = battle_over.capitalize()
                
                    if ('out of' in battle_over and 'usable' in battle_over) or ('Player' in battle_over and 'defeated' in battle_over):
                        print('battle over')
                        while get_color(1043,515) == (200,168,72) and get_color(1043,533) == (40,80,104):
                            pyd.press('z')
                        exit()
                        
                    elif 'make' in after_moves and 'room' in after_moves:

                    time.sleep(0.25)

                x = 1180
                while x <= 1468:
                    if get_color(x,618) == (248,0,0):
                        pyd.press('z')
                        break
                    x += 2
            
            # check for opp faint
            # change the border to be top left
        
        switch_after_faint = False
        check_my_move = False
        forced_switch = False
        make_move = False
    
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