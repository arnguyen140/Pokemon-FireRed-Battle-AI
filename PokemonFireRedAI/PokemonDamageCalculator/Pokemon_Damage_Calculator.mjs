import {calculate, Generations, Pokemon, Move, Field} from '@smogon/calc';

const gen = Generations.get(3); // alternatively: const gen = 5;

function getdamage(atk_mon, atk_lvl, atk_ivs, atk_stat1, spa_stat1, spe_stat1, def_mon, def_lvl, def_ivs, def_stat2, spd_stat2, spe_stat2, reflect_on, lightscreen_on, status_atk, status_def, HP_amount, move, max_min) {
  const result = calculate(
    gen,
    new Pokemon(gen, atk_mon, {
      level: atk_lvl,
      nature: 'Bashful',
      ivs: {hp: atk_ivs, atk: atk_ivs, def: atk_ivs, spa: atk_ivs, spd: atk_ivs, spe: atk_ivs},
    }),
    new Pokemon(gen, def_mon, {
      level: def_lvl,
      nature: 'Bashful',
      ivs: {hp: def_ivs, atk: def_ivs, def: def_ivs, spa: def_ivs, spd: def_ivs, spe: def_ivs},
    }),
    new Move(gen, move)
  );

  const result2 = calculate(
    gen,
    new Pokemon(gen, atk_mon, {
      level: atk_lvl,
      nature: 'Bashful',
      ivs: {hp: atk_ivs, atk: atk_ivs, def: atk_ivs, spa: atk_ivs, spd: atk_ivs, spe: atk_ivs},
      boosts: {atk: atk_stat1, def: 0, spa: spa_stat1, spd: 0, spe: spe_stat1},
      status: status_atk,
      curHP: (HP_amount/100) * result.attacker.originalCurHP,
    }),
    new Pokemon(gen, def_mon, {
      level: def_lvl,
      nature: 'Bashful',
      ivs: {hp: def_ivs, atk: def_ivs, def: def_ivs, spa: def_ivs, spd: def_ivs, spe: def_ivs},
      boosts: {atk: 0, def: def_stat2, spa: 0, spd: spd_stat2, spe: spe_stat2},
      status: status_def,
    }),
    new Move(gen, move),
    new Field({
      defenderSide: {isReflect: reflect_on, isLightScreen: lightscreen_on}
    }),
  );
  if (max_min === 'min') {
    // console.log((Math.floor(((result2.damage[0]/result2.defender.stats.hp) * 100) * 100) / 100), result2.attacker.stats.spe, result2.defender.stats.spe)
    var move_damage = result2.damage[0]
  }
  else {
    // console.log((Math.floor(((result2.damage[15]/result2.defender.stats.hp) * 100) * 100) / 100), result2.attacker.stats.spe, result2.defender.stats.spe)
    var move_damage = result2.damage[15]
  }
  console.log((Math.floor(((move_damage/result2.defender.stats.hp) * 100) * 100) / 100), result2.attacker.stats.spe, result2.defender.stats.spe)
  // return (Math.floor(((result.damage[0]/result.defender.rawStats.hp) * 100) * 100) / 100);
}

const atk_mon = process.argv[2]
const atk_lvl = parseInt(process.argv[3])
const atk_ivs = parseInt(process.argv[4])
const atk_stat1 = parseInt(process.argv[5])
const spa_stat1 = parseInt(process.argv[6])
const spe_stat1 = parseInt(process.argv[7])
const def_mon = process.argv[8]
const def_lvl = parseInt(process.argv[9])
const def_ivs = parseInt(process.argv[10])
const def_stat2 = parseInt(process.argv[11])
const spd_stat2 = parseInt(process.argv[12])
const spe_stat2 = parseInt(process.argv[13])
var reflect_on = (process.argv[14] === 'true')
var lightscreen_on = (process.argv[15] === 'true')
const status_atk = process.argv[16]
const status_def = process.argv[17]
const HP_amount = parseInt(process.argv[18])
const move = process.argv[19]
const max_min = process.argv[20]

getdamage(atk_mon, atk_lvl, atk_ivs, atk_stat1, spa_stat1, spe_stat1, def_mon, def_lvl, def_ivs, def_stat2, spd_stat2, spe_stat2, reflect_on, lightscreen_on, status_atk, status_def, HP_amount, move, max_min)

// console.log(getdamage('Gengar', 'Chansey', 50, 50, 'Fire Punch'))