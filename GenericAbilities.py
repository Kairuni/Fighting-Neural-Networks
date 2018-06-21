from Afflictions import aff_id;
from Afflictions import aff;
from Tests import *;

def freezeAffs(targ):
    if (aff("shivering") in targ.affs):
        return "frozen";
    elif (aff("no_caloric") in targ.affs):
        return "shivering";
    else:
        return "no_caloric";

def asthma(targ):
    if (aff("no_fitness") in targ.affs):
        return "asthma";
    else:
        return "no_fitness";

def cripple(targ):
    if (aff("crippled") in targ.affs):
        return "crippled_body";
    else:
        return "crippled";

def disrupt(targ):
    if (aff("mental_disruption") in targ.affs):
        return "physical_disruption";
    else:
        return "mental_disruption";

conversion = {
    "asthma": asthma,
    "freeze": freezeAffs,
    "disrupt": disrupt,
    "cripple": cripple,
}


def genAb(
            NAME,
            ## Afflictions
            affList = None, durations = {},
            stack = {}, visible = {},
            stateNeeded = {},

            hardStateNeeded = {},

            ## Venoms:
            numVenoms = 0,

            ## Balance function and hp/mp damage.
            balFunc = [consumeBalEq, 1.0], hpDmg = 0.0, mpDmg = 0.0,
            ## Limb damage stuff
            limbDmg = None, limbEffect = 0, doBreak = 1, limbsRequired = 0,
            ## Preventative measures
            numArmsNeeded = 1, stopAffList = None, stopDefList = None,
            ## Room mechanics
            roomFlags = None,
            ## Class mechanics
            updateState = None,
            ## Target required
            targReq = True,
            ## Prone
            notProne = True,
            ## Bleed
            bleedDmg = 0,
            ## Rebounding
            hitRebounding = False,
			## Do clumsy check
			testClumsy = False,
			## Do dodging check
			isDodgeable = False,
            ):
    armTest = oneArmCheck;
    if (numArmsNeeded == 2):
        armTest = bothArmCheck;

    if (affList or numVenoms > 0):
        if (not affList):
            affList = {};

        for i in range(len(affList) + numVenoms):
            if (i not in durations):
                durations[i] = 0;

        for i in range(len(affList) + numVenoms):
            if (i not in stack):
                stack[i] = 0;

        for i in range(len(affList) + numVenoms):
            if (i not in stateNeeded):
                stateNeeded[i] = [None, None];

        for i in range(len(affList) + numVenoms):
            if (i not in visible):
                visible[i] = [True, True];

    def newAb(self, targ, limbTarget = None, venoms = None):
        if (not targ and targReq):
            return False;

        for state in hardStateNeeded:
            preReqs = True;
            if (isinstance(state[1], str)):
                if (self.classState[state[0]] != state[1]):
                    preReqs = False;
            else:
                if (self.classState[state[0]] < state[1]):
                    preReqs = False;

            if (not preReqs):
                print(self.name,"state",state[0],"not",state[1],"for",NAME,"current:",self.classState[state[0]]);
                return False;

        ## If we require limbs and the user didn't provide enough limbs, end it.
        if (limbsRequired > 0 and len(limbTarget) != limbsRequired):
            return False;

        if (notProne and testProne(self)):
            return False;

        ## If we were given a stopAffList, test it.
        if (stopAffList):
            for affliction in stopAffList[0]:
                if (aff(affliction) in self.affs):
                    return False;
            for affliction in stopAffList[1]:
                if (aff(affliction) in targ.affs):
                    return False;

        ## If we've hit this point, then we test arms and the balance function. If both true, we do stuff.
        if (armTest(self) and balFunc[0](self, balFunc[1])):
            if (hitRebounding and not (aff("no_rebounding") in targ.affs)):
                targ = self;

            if (targ):
                print(self.name + " " + NAME + " " + targ.name, end = " ");
                if (numVenoms > 0):
                    print("(", end = "");
                    first = True;
                    for venom in venoms:
                        if (not first):
                            print(" ", end = "");
                        print(venom, end = "");
                        first = False;
                    print(")", end = "");
                print();
            else:
                print(self.name + " " + NAME);
            localAffList = [];
            if (affList):
                for val in affList:
                    localAffList.append(val);

            for i in range(numVenoms):
                if (i < len(venoms)):
                    localAffList.append([None, venoms[i]]);

            ## Test limb damage.
            if (limbsRequired > 0):
                i = 0;
                for limb in limbTarget:
                    ## Standard limb damage
                    if (limbEffect == 0):
                        targ.takeLimbDmg(limb, limbDmg[i]);
                    ## Limb damage with no break (i.e. frenzy)
                    elif (limbEffect == 1):
                        targ.takeLimbDmg(limb, limbDmg[i], False);

                    ## Auto-cripple/damage/mangle the given limb (shifter).
                    if (limbEffect == 2 and limb not in ["head", "torso"]):
                        targ.addAff(aff(limb + "_broken"));
                    elif (limbEffect == 3 and aff(limb + "_broken") in targ.affs):
                        targ.addAff(aff(limb + "_damaged"));
                    elif (limbEffect == 4 and aff(limb + "_damaged") in targ.affs):
                        targ.addAff(aff(limb + "_mangled"));

                    i += 1;

            ## For all our affs, do stuff.
            i = 0;

            for pair in localAffList:
                preReqs = False;
                if (isinstance(pair[0], list)):
                    preReqs = True;
                    for preReq in pair[0]:
                        if (not (aff(preReq) in targ.affs)):
                            preReqs = False;

                elif (pair[0] == None or aff(pair[0]) in targ.affs):
                    preReqs = True;

                if (stateNeeded[i][0] != None):
                    if (isinstance(stateNeeded[i][1], str)):
                        if (self.classState[stateNeeded[i][0]] != stateNeeded[i][1]):
                            preReqs = False;
                    else:
                        if (self.classState[stateNeeded[i][0]] < stateNeeded[i][1]):
                            preReqs = False;

                if (preReqs):
                    ## Bit of repeated code here, but that's probably the least of my sins.
                    if (isinstance(pair[1], list)):
                        for listedAff in pair[1]:
                            if (listedAff in conversion):
                                listedAff = conversion[listedAff](targ);

                            targ.addAff(aff(listedAff), duration = durations[i]);

                    else:
                        if (pair[1] in conversion):
                            pair[1] = conversion[pair[1]](targ);

                        targ.addAff(aff(pair[1]), stacks = stack[i], duration = durations[i], selfVis = visible[0], applierVis = visible[1]);

                i += 1;

            if (targ):
                targ.takeDmg(hpDmg, mpDmg);
                targ.bleed += bleedDmg;

            ## Update room flags.
            if (roomFlags):
                for flag in roomFlags:
                    #print(flag);
                    if (flag[1]):
                        self.room.setFlag(flag[0], flag[1], flag[2]);
                    else:
                        self.room.clearFlag(flag[0]);

            ## Update class states
            if (updateState):
                for entry in updateState:
                    if (len(entry) < 3):
                        self.classState[entry[0]] = entry[1];
                    elif (entry[1] > 0 and self.classState[entry[0]] < entry[2]):
                        self.classState[entry[0]] = self.classState[entry[0]] + entry[1];
                        if (self.classState[entry[0]] > entry[2]):
                            self.classState[entry[0]] = entry[2];
                    elif (entry[1] < 0 and self.classState[entry[0]] > entry[2]):
                        self.classState[entry[0]] = self.classState[entry[0]] + entry[1];
                        if (self.classState[entry[0]] < entry[2]):
                            self.classState[entry[0]] = entry[2];

                chargeMin = min(self.classState['l_charge'], self.classState['r_charge']);
                self.classState['b_charge'] = chargeMin;

            return True;
        else:
            return False;

    return newAb;
