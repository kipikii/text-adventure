### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
from random import *    
from math import *
from time import *

class Spell:
    # self, mana cost, number of casts, stat to use, power of attack (multiplier), chance to hit, damage take on cast (multiplier), effects to enemy, effects to caster, victim var, attacker var
    def __init__(self, name, cost, procs, dmgStat, hitStat, damage, damageRecoil, applyEffect, givesEffect):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.procs = procs
        self.dmgStat = dmgStat
        self.hitStat = hitStat
        self.damageRecoil = damageRecoil
        self.applyEffect = applyEffect
        self.givesEffect = givesEffect

class Monster:
    def __init__(self, name: str, HP: int, STR: int, DEX: int, DEF: int, AGI: int, skills: list):
        self.name = name
        self.HP = HP
        self.MaxHP = self.HP
        self.MP = inf
        self.MaxMP = inf
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.AGI = AGI
        self.skills = skills
        self.status = [ ]
    def skillSelect(self, skills: list):
        toUse = skills[random.randint(0, (len(skills)-1))]
        print(toUse)

class Equipment:
    def __init__(self, slot, BonusHP, BonusMP, BonusSTR, BonusDEX, BonusDEF, BonusAGI, special):
        self.slot = slot
        self.BonusHP = BonusHP
        self.BonusMP = BonusMP
        self.BonusSTR = BonusSTR
        self.BonusDEX = BonusDEX
        self.BonusDEF = BonusDEF
        self.BonusAGI = BonusAGI
        self.special = special

class Player:
    def __init__(self, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int):
        self.level = 1
        self.HP = HP
        self.MaxHP = HP
        self.MP = MP
        self.MaxMP = MP
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.AGI = AGI
        self.skills = [ ]
        self.status = [ ]
        self.weapon = None
        self.head = None
        self.chest = None
        self.legs = None
        self.charm = None

def calcHit(victimAGI: int, attackerDEX: int):
    # roll for agi proc. if fail, hit
    if (victimAGI < 0): victimAGI = 0
    if (attackerDEX < 0): attackerDEX = 0
    if (victimAGI == 3): 
        hitChance = round(log(((attackerDEX + 1) * (2.999999 / (victimAGI + 1.0000001)))) * 40) + 45
    else: 
        hitChance = round(log((attackerDEX + 1) * (3 / (victimAGI + 1.0000001))) * 40) + 45
    if (hitChance < 30): hitChance = 30
    if (hitChance >= randint(1,100)): return True
    else: return False

#cost, procs, dmgStat, hitStat, damage, damageRecoil, applyEffect, givesEffect
#mana cost, number of casts, stat to use for dmg, stat to use for hit, power of attack (multiplier), chance to hit, damage take on cast (multiplier), effects to enemy, effects to caster, victim var, attacker var
def castSpell(spell, caster, victim):
    print("the " + caster.name + " attacks!")
    for each in range(spell.procs):
        if (calcHit(eval("caster." + str(spell.hitStat)), victim.AGI)):
            damage = round((eval("caster." + str(spell.dmgStat)) * (randint(90, 120)/100)) - victim.DEF)
            if (damage <= 0):
                print("0 damage")
            else:
                print(str(damage) + " damage")
                victim.HP -= damage
        else:
            print("miss")
    print("your hp: " + str(victim.HP) + " / " + str(victim.MaxHP))

def verify(question:str=None, allowed:list=None):
    while (True):
        if (allowed == None):
            print("no given list for verify, returned statement")
            return
        if (question == None):
            chosen = input("what will you do? ")
        else:
            chosen = input(question)
        for i in allowed:
            if (chosen == i):
                return chosen

spells = {
    "attack": Spell("attack", 0, 1, "STR", "DEX", 1, 0, [ ], [ ]),
    "doublecut": Spell("doublecut", 5, 2, "STR", "DEX", 1.25, 0, [ ], [ ]),
    "bolt": Spell("bolt", 5, 1, "MP", "AGI", .5, 0, [], []),
}

monsters = {
    "rat": Monster("rat", 3, 2, 0, 0, 0, ["attack"]),
    "wolf": Monster("wolf", 10, 3, 3, 1, 0, ["attack"]),
    "imp": Monster("imp", 15, 4, 5, -3, 0, ["attack", "bolt"]),
    "dummy" : Monster("dummy", 100, 10, 10, 10, 10, ["attack"])
}

player = Player(100, 10, 10, 10, 10, 10)

enemy = monsters["dummy"]
castSpell(spells["attack"], enemy, player)

hits = 0
misses = 0
print("")
print("agi: " + str(player.AGI))
print("dex: " + str(enemy.DEX))
print('out of 10000 hits:')
for i in range(10000):
    x = calcHit(player.AGI, enemy.DEX)
    if (x): hits += 1
    else: misses += 1
print("hits: " + str(hits))
print("misses: " + str(misses))
print("hit percentage: " + str(hits/100) + "%")
