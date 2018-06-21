from Afflictions import aff_id;
from Afflictions import aff;

def oneArmCheck(self):
	return not (aff("left_arm_broken") in self.affs) or not (aff("right_arm_broken") in self.affs);

def bothArmCheck(self):
	return not (aff("right_arm_broken")) in self.affs and not (aff("left_arm_broken") in self.affs);

def checkBalEq(self):
	return self.balances[0] <= 0 and self.balances[1] <= 0;

def checkDelay(self):
	return "delay" in self.defs;

def checkAff(targ, aff):
	return aff in targ.affs;

def testProne(targ):
	testList = [aff("prone"), aff("frozen"), aff("indifference"), aff("unconscious"), aff("asleep"), aff("stun"), aff("paralysis")];

	testMin = aff("writhe_armpitlock");
	testMax = aff("writhe_feed");

	for affl in testList:
		if (affl in targ.affs):
			return True;

	for i in range(testMin, testMax + 1):
		if (i in targ.affs):
			return True;

	return False;

def noConsumeBalEq(self, amount):
	if (checkBalEq(self)):
		return True;
	return False;

def consumeEqBal(self, amount):
	if (checkBalEq(self)):
		self.balances[1] = amount;
		return True;
	return False;

def consumeBalEq(self, amount):
	if (checkBalEq(self)):
		self.balances[0] = amount;
		return True;
	return False;

def consumeSecondary(self, amount):
	if (checkBalEq(self) and self.balances[4] <= 0):
		self.balances[4] = amount;
		return True;
	return False;

def consumeElixir(self, amount):
	if (self.balances[2] and not aff("anorexia") in self.affs):
		self.balances[2] = amount;
		return True;
	return False;

# bal, eq, elixir, affelixir, ability, right_arm, left_arm, herb, focus, tree, salve, pipe, renew, moss
