import subprocess

# process = subprocess.Popen(['node', 'Pokemon_Damage_Calculator.mjs'], stdout=subprocess.PIPE)
# print (process.communicate()[0])

# Subprocess searches for a module/file that is in the path of the folder that is opened in VScode
def calc_move(plyr_pokemon,opp_pokemon,plyr_lvl,opp_lvl,move):
    process = subprocess.check_output(['node', 'PokemonDamageCalculator\Pokemon_Damage_Calculator.mjs',plyr_pokemon,opp_pokemon,plyr_lvl,opp_lvl,move])
    process = float(process.decode("utf-8"))
    return process

print(calc_move('Gengar','Chansey',str(50),str(50),'Focus Punch'))