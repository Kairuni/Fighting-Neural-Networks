from GenericAbilities import *


BF = "BATTLEFURY ";
BFI = "BLADEFIRE ";

TemplarSkills = [
	# Battlefury
	genAb(BF+"DSK", numVenoms = 2, balFunc = [consumeBalEq, 2.19], numArmsNeeded = 2, hpDmg = 1.0, hitRebounding = True, updateState = [['l_charge', 24, 175], ['r_charge', 24, 175]]),
	genAb(BF+"RSK", numVenoms = 1, affList = [[None, "no_rebounding"]], balFunc = [consumeBalEq, 2.19], numArmsNeeded = 2, hpDmg = 1.0, updateState = [['r_charge', 24, 175]]),

	# Bladefire
	genAb(BFI+"VORPAL", numVenoms = 1, balFunc = [noConsumeBalEq, 0.0], numArmsNeeded = 2, hardStateNeeded = [['b_charge', 150]], updateState = [['l_charge', 0], ['r_charge', 0]]),

    genAb(BFI+"RETRIBUTION", balFunc = [consumeBalEq, 5],
            numArmsNeeded = 2, affList = [[ ["paralysis", "crippled_body", "mental_disruption", "physical_disruption"], "death"]]),
];

TemplarPassives = [

];
