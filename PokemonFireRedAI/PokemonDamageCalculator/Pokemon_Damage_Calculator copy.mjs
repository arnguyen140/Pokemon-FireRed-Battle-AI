import {calculate, Generations, Pokemon, Move, Field} from '@smogon/calc';

const gen = Generations.get(5); // alternatively: const gen = 5;
function getdamage(reflect_on,lightscreen_on,max_min) {
  const result = calculate(
    gen,
    new Pokemon(gen, 'Gengar', {
      item: 'Choice Specs',
      nature: 'Timid',
      evs: {spa: 252},
      boosts: {spa: 1},
    }),
    new Pokemon(gen, 'Chansey', {
      item: 'Eviolite',
      nature: 'Calm',
      evs: {hp: 252, spd: 252},
    }),
    new Move(gen, 'Focus Blast'),
    new Field({
      defenderSide: {isReflect: reflect_on,isLightScreen: lightscreen_on}
    }),
  );
  if (max_min === 'min'){
    console.log(result.damage[0])
  }
  else {
    console.log(result.damage[15])
  }
  }

var reflect_on = (process.argv[2] === 'true')
var lightscreen_on = (process.argv[3] === 'true')
const max_min = process.argv[4]

getdamage(reflect_on,lightscreen_on,max_min)