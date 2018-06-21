import time;
from Afflictions import aff_id;
from Afflictions import aff;
from Tests import *;

FLOAT_TOLERANCE = 0.000000000001;

tickAffs = [aff("ablaze"), aff("dizziness"), aff("punished_arms"), aff("paresis")];

class Actor:
	pillCures = {
		"antipsychotic" : [aff("sadness"), aff("confusion"), aff("dementia"), aff("hallucinations"), aff("paranoia"), aff("hypersomnia"), aff("hatred"), aff("addiction"), aff("blood_curse"), aff("blighted")],
		"euphoriant" : [aff("self-pity"), aff("stupidity"), aff("dizziness"), aff("faintness"), aff("shyness"), aff("epilepsy"), aff("impatience"), aff("dissonance"), aff("infested"), aff("insomnia")],
		"decongestant" : [aff("baldness"), aff("clumsiness"), aff("hypochondria"), aff("weariness"), aff("asthma"), aff("sensitivity"), aff("ringing_ears"), aff("impairment"), aff("blood_poison")],
		"depressant" : [aff("commitment_fear"), aff("merciful"), aff("recklessness"), aff("egocentric"), aff("masochism"), aff("agoraphobia"), aff("loneliness"), aff("berserking"), aff("vertigo"), aff("claustrophobia")],
		"coagulation" : [aff("body_odor"), aff("lethargy"), aff("allergies"), aff("mental_disruption"), aff("physical_disruption"), aff("vomiting"), aff("exhausted"), aff("thin_blood"), aff("rend"), aff("haemophilia")],
		"steroid" : [aff("hubris"), aff("pacifism"), aff("peace"), aff("lovers_effect"), aff("laxity"), aff("superstition"), aff("generosity"), aff("justice"), aff("magnanimity")],
		"opiate" : [aff("paresis"), aff("paralysis"), aff("TREE_PARALYSIS"), aff("mirroring"), aff("crippled_body"), aff("crippled"), aff("blisters"), aff("slickness"), aff("heartflutter"), aff("sandrot")],
		"panacea" : [aff("patterns")],
		"amaurosis" : [aff("no_blindness")],
		"ototoxin" : [aff("no_deafness")],
		"anabiotic" : [aff("bulimia"), aff("plodding"), aff("idiocy")],
		"waterbreathing" : [aff("no_waterbreathing")],
		"acuity" : [aff("no_thirdeye")],
		"thanatonin" : [aff("no_deathsight")],
		"kawhe" : [aff("no_insomnia")],
		"stimulant" : [aff("no_instawake")],
	}


	def __init__(self, Name, classSkills):
		self.name = Name;
		self.hp = 100.0;
		self.mp = 100.0;
		self.bleed = 0.0;
		self.limbs = {"head": 0.0, "torso": 0.0, "left_arm": 0.0, "right_arm": 0.0, "left_leg": 0.0, "right_leg": 0.0};
		self.affs = {};
		self.tickableAffs = {};
		self.inhibitedCures = {};
		self.defs = {};
		self.tickableDefs = {};
		self.skills = [];
		self.curTime = 0;
		self.firstAid = None;

		for skill in classSkills:
			self.skills.append(skill);
		#for skill in Actor.defaultSkills:
		#	self.skills.append(skill);

		self.classState = {'resonance': None, 'soul': 0.0, 'energy': 0.0, 'kai': 0.0, 'l_charge': 0, 'r_charge': 0, 'b_charge': 0};
						# bal, eq, elixir, affelixir, ability, right_arm, left_arm, herb, focus, tree, salve, pipe, renew, moss
		self.balances = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		self.room = None;
		self.avgAffDuration = 0.0;
		self.avgAffDurationCount = 0;

	def tickBals(self, time):
		for i in range(len(self.balances)):
			self.balances[i] -= time;

	def takeDmg(self, hpDmg = 0, mpDmg = 0):
		if (hpDmg >= FLOAT_TOLERANCE):
			self.hp -= hpDmg;
		if (mpDmg >= FLOAT_TOLERANCE):
			self.mp -= mpDmg;

	def healDmg(self, hpHeal = 0, mpHeal = 0):
		if (hpDmg >= FLOAT_TOLERANCE):
			self.hp += hpDmg;
			if (self.hp > 100.0):
				self.hp = 100.0;
		if (mpDmg >= FLOAT_TOLERANCE):
			self.mp += mpDmg;
			if (self.mp > 100.0):
				self.mp = 100.0;

	def takeLimbDmg(self, limb, dmg, doBreak = True):
		if (limb in self.limbs):
			self.limbs[limb] += dmg;
			if (not doBreak):
				return;

			if (self.limbs[limb] > 1/3 * 100):
				if (limb not in ["head", "torso"]):
					self.addAff(aff(limb + "_broken"));
				self.addAff(aff(limb + "_damaged"));

			if (self.limbs[limb] > 2/3 * 100):
				if (limb not in ["head", "torso"]):
					self.addAff(aff(limb + "_broken"));
				self.addAff(aff(limb + "_damaged"));
				self.addAff(aff(limb + "_mangled"));


	def printState(self):
		print(self.hp, self.mp, end="|");

		for aff in self.affs:
			print(aff_id(aff), ":", self.affs[aff][0], self.affs[aff][1], self.affs[aff][2], self.affs[aff][3], end="|");

		print();

	def addAff(self, affl, stacks = 0, duration = 0, timer = 0, selfVis = True, applierVis = True):
		if (stacks != 0 and affl in self.affs):
			stacks = self.affs[affl][1] + stacks;
			self.affs[affl] = [self.affs[affl][0], stacks, duration, self.affs[affl][3]];
		else:
			self.affs[affl] = [self.curTime, stacks, duration, timer];

		if (affl in tickAffs):
			self.tickableAffs[affl] = True;

		if (affl == aff("death")):
			print(self.name + " HAS DIED");

	def remAff(self, affl):
		if (affl in self.affs):
			self.avgAffDuration += (self.curTime - self.affs[affl][0]);
			self.avgAffDurationCount += 1;

		self.affs.pop(affl, None);
		self.tickableAffs.pop(affl, None);

	def hasAff(self, aff):
		return aff in self.affs;

	def tickAffs(self, time):
		remList = [];
		addList = [];
		for affl in self.tickableAffs:
			if (affl == aff("ablaze")):
				if (self.affs[affl][3] >= 10 or self.affs[affl][1] == 0):
					self.takeDmg(1 + 1 * self.affs[affl][1]);
					self.affs[affl][1] += 1;
					self.affs[affl][3] = 0;
			elif (affl == aff("paresis")):
				if (self.affs[affl][3] >= 5):
					remList.append(affl);
					addList.append(aff("paralysis"));

			self.affs[affl][3] += time;
			if (self.affs[affl][2] != 0 and self.affs[affl][3] > self.affs[affl][2]):
				remList.append(affl);

		for rem in remList:
			self.remAff(rem);
		for add in addList:
			self.addAff(add);


	def addDef(self, defense, skill, ability, target, timer, duration):
		self.defs[defense] = [skill, ability, target, timer, duration];

	def remDef(self, defense):
		self.defs.pop(defense, None);

	def tickDefs(self, time):
		for defense in self.tickableDefs:
			print(defense);

	def tickRestoration(self, time):
		if (self.restoration):
			self.restoration[0] -= time;
			if (self.restoration[0] <= 0):
				print("TODO: CURED A LIMB");

	def tick(self, time):
		self.curTime += time;
		self.curTime = round(self.curTime, 2);
		self.tickAffs(time);
		self.tickDefs(time);
		self.tickBals(time);
		#self.printState();

		if (self.firstAid):
			self.firstAid(self);

	def resetBals(self):
		for i in range(len(self.balances)):
			self.balances[i] = 0;

	## TODO: Make these function
	def eatPill(self, pill):
		print("Eating",pill);

	def applySalve(self, salve, location):
		print("Applying",salve,location);

	def smokePipe(self, pipe):
		print("Smoking",pipe);

	def sipElixir(self, elixir):
		print("Sipping", elixir);

	def focus(self):
		print("Focusing");

	def renew(self):
		print("Renewing");



class Room:
	def __init__(self):
		self.flags = {};
		self.actors = [];
		self.timer = 0;

	def setFlag(self, flag, value, timeout):
		self.flags[flag] = [value, timeout];

	def clearFlag(self, flag):
		#print("Clearing flag" + flag);
		self.flags.pop(flag, None);

	def tickFlags(self, time):
		popList = [];
		for flag in self.flags:
			self.flags[flag][1] -= time;
			if (self.flags[flag][1] <= 0):
				popList.append(flag);
		for flag in popList:
			self.flags.pop(flag, None);

	def tickActors(self, time):
		for actor in self.actors:
			actor.tick(time);

	def tick(self, time):
		self.timer += time;
		self.tickFlags(time);
		self.tickActors(time);

	def addActor(self, actor):
		self.actors.append(actor);
		actor.room = self;
