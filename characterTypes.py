import random

baseDodgeChance = 20

def levelup(time, attributes):
    attributeNames = []
    for i in attributes:
        attributeNames.append(i)

    for i in range(time):
        for i in range(random.randint(1, 3)):
            attributes[random.choice(attributeNames)] += 1

    return attributes

class character():

    baseDmg = 3
    baseHitpoint = 50

    def __init__(self, str, dex, con,lv):
        self.attributes = {
            "strength": str,
            "dexteriety": dex,
            "constitution": con
        }
        self.level = lv
        self.attributes = levelup(lv - 1, self.attributes)

    def stats(self):
        self.hitPoint = self.baseHitpoint + self.attributes["constitution"] * 10

    def attack(self, enemy):

        if random.randint(1, 100) < baseDodgeChance +\
                (self.attributes["dexteriety"] - enemy.attributes["dexteriety"]) * 2:
            attackDmg = "You missed"
        else:
            attackDmg = self.baseDmg + self.attributes["strength"] * 3

        return attackDmg



class player(character):

    experience = 0


    def __init__(self, str, dex, con, lv):
        super().__init__(str, dex, con, lv)
        self.expToNextLevel = 100 * lv
        self.baseDmg = 5
        self.baseHitpoint = 100

    def playerLevelUp(self):

        levelTimes = 0
        while self.experience >= self.expToNextLevel:
            self.experience -= self.expToNextLevel
            self.expToNextLevel += 100
            levelTimes += 1
            self.level += 1

        self.attributes = levelup(levelTimes, self.attributes)

    def fled(self, enemy):

        return random.randint(1, 100) < 50 + (self.attributes["dexteriety"] - enemy.attributes["dexteriety"]) * 2