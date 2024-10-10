### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
from random import *    
from math import *
from time import *

class Spell:
    # self, mana cost, number of casts, stat to use, power of attack (multiplier), chance to hit, damage take on cast (multiplier), effects to enemy, effects to caster, victim var, attacker var
    def __init__(self, cost, procs, dmgStat, hitStat, damage, damageRecoil, applyEffect, givesEffect):
        self.cost = cost
        self.damage = damage
        self.procs = procs
        self.dmgStat = dmgStat
        self.hitStat = hitStat
        self.damageRecoil = damageRecoil
        self.applyEffect = applyEffect
        self.givesEffect = givesEffect

class Monster:
    def __init__(self, name, HP, STR, DEX, DEF, skills: list):
        self.name = name
        self.HP = HP
        self.MaxHP = self.HP
        self.MP = inf
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.skills = skills
        self.status = [ ]
    def skillSelect(self, skills: list):
        toUse = skills[random.randint(0, (len(skills)-1))]
        print(toUse)

class Equipment:
    def __init__(self, slot, BonusHP, BonusMP, BonusSTR, BonusDEX, BonusDEF, special):
        self.slot = slot
        self.BonusHP = BonusHP
        self.BonusMP = BonusMP
        self.BonusSTR = BonusSTR
        self.BonusDEX = BonusDEX
        self.BonusDEF = BonusDEF
        self.special = special

class Player:
    def __init__(self, HP: int, MP: int, STR: int, DEX: int, DEF: int):
        self.level = 1
        self.HP = HP
        self.MP = MP
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.skills = [ ]
        self.status = [ ]
        self.weapon = None
        self.head = None
        self.chest = None
        self.legs = None
        self.charm = None

#cost, procs, dmgStat, hitStat, damage, damageRecoil, applyEffect, givesEffect
#mana cost, number of casts, stat to use for dmg, stat to use for hit, power of attack (multiplier), chance to hit, damage take on cast (multiplier), effects to enemy, effects to caster, victim var, attacker var
def castSpell(spell, caster, victim):
    print("spell cost: " + str(spell.cost))
    for each in range(spell.procs):
        print("stat for hit: " + str(spell.hitStat) + ", " + str(eval("caster." + str(spell.hitStat))))
        print("stat for damage: " + str(spell.dmgStat) + ", " + str(eval("caster." + str(spell.dmgStat))))

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
    "attack": Spell(0, 1, "STR", "DEX", 1, 0, [ ], [ ]),
    "doublecut": Spell(5, 2, "STR", "DEX", 1.25, 0, [ ], [ ])
}

monsters = {
    "rat": Monster("rat", 3, 2, 0, 0, ["attack"]),
    "wolf": Monster("wolf", 10, 3, 1, 1, ["attack"]),
    "imp": Monster("imp", 15, 4, 5, -3, ["attack", "flame"])
}

player = Player(100, 100, 10, 10, 10)

enemy = monsters["wolf"]
print("the " + enemy.name + " attacked for " + str(enemy.STR) + " damage")
castSpell(spells["attack"], enemy, player)