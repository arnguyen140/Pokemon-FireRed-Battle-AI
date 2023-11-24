import {calculate, Generations, Pokemon, Move} from '@smogon/calc';

const gen = Generations.get(3); // alternatively: const gen = 5;

function getdamage(atk_mon,atk_lvl,atk_ivs,atk_stat1,spa_stat1,spe_stat1,def_mon,def_lvl,def_ivs,def_stat2,spd_stat2,spe_stat2,HP_amount,move) {
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
      curHP: (HP_amount/100) * result.attacker.originalCurHP,
    }),
    new Pokemon(gen, def_mon, {
      level: def_lvl,
      nature: 'Bashful',
      ivs: {hp: def_ivs, atk: def_ivs, def: def_ivs, spa: def_ivs, spd: def_ivs, spe: def_ivs},
      boosts: {atk: 0, def: def_stat2, spa: 0, spd: spd_stat2, spe: spe_stat2},
    }),
    new Move(gen, move)
  );

  // if (max_min == 0) {
  //   damage = result.damage[0]
  // }
  // else {
  //   damage = result.damage[15]
  // }
  
  // return (Math.floor(((result.damage[0]/result.defender.rawStats.hp) * 100) * 100) / 100);
  console.log((Math.floor(((result2.damage[15]/result2.defender.stats.hp) * 100) * 100) / 100),result2.attacker.stats.spe,result2.defender.stats.spe)

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
const HP_amount = parseInt(process.arg[14])
const move = process.argv[15]
// const max_min = parseInt(process.arg[15])

getdamage(atk_mon,atk_lvl,atk_ivs,atk_stat1,spa_stat1,spe_stat1,def_mon,def_lvl,def_ivs,def_stat2,spd_stat2,spe_stat2,HP_amount,move)

// console.log(getdamage('Gengar','Chansey',50,50,'Fire Punch'))