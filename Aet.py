import time;

from ActorsRooms import Actor;
from ActorsRooms import Room;
from Ascendril import AscendrilSkills;
from Ascendril import AscendrilPassives;
from Templar import TemplarSkills;
from Templar import TemplarPassives;
from FirstAid import FirstAid;
from Afflictions import aff;
from Afflictions import aff_id;

C1 = Actor("C1", AscendrilSkills);
C2 = Actor("C2", TemplarSkills);
C1.firstAid = FirstAid;

testRoom = Room();
testRoom.addActor(C1);
testRoom.addActor(C2);

AscendrilSkills[4](C1, None);
testRoom.tick(5);
AscendrilSkills[1](C1, None);
testRoom.tick(5);

TemplarSkills[1](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["paresis", "asthma"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[0](C2, C1, venoms = ["slickness", "anorexia"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[1](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["disrupt", "disrupt"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[3](C2, C1);
testRoom.tick(6);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["cripple", "cripple"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["vomiting", "haemophilia"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["stupidity", "clumsiness"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["stupidity", "clumsiness"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["stupidity", "clumsiness"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[0](C2, C1, venoms = ["stupidity", "clumsiness"]);
testRoom.tick(2.19);
C1.printState();
TemplarSkills[2](C2, C1, venoms = ["asthma"]);
TemplarSkills[3](C2, C1);
testRoom.tick(6);
C1.printState();



print ("Ticking test room.");

while (testRoom.timer < 1200):
	testRoom.tick(0.01);

print("Done ticking test room.");
#print(Actor.pillCures);
