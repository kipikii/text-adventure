### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
from random import *    
from math import *
from time import *
from copy import *

class Spell:
    # self, mana cost, number of casts, stat to use, power of attack (multiplier), stat for hit, damage take on cast (multiplier), effects to enemy, effects to caster, ignore enemy defense
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damage: float, damageRecoil: float, ignoreEnemy: bool, applyEffect: list, givesEffect: list):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.procs = procs
        self.dmgStat = dmgStat
        self.hitStat = hitStat
        self.damageRecoil = damageRecoil
        self.ignoreEnemy = ignoreEnemy
        self.applyEffect = applyEffect
        self.givesEffect = givesEffect

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

class Entity:
    def __init__(self, name, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list, blessings: list):
        self.level = 1
        self.name = name
        self.HP = HP
        self.MaxHP = HP
        self.MP = MP
        self.MaxMP = MP
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.AGI = AGI
        self.spells = spells
        self.status = [ ]
        self.blessings = blessings
        self.weapon = None
        self.head = None
        self.chest = None
        self.legs = None
        self.charm = None

    def skillSelect(self, skills: list):
        skills += ["attack"]
        toUse = skills[randint(0, (len(skills)-1))]
        return toUse

spells = {
    "attack": Spell("attack", 0, 1, "STR", "DEX", 1, 0, False,[ ], [ ]),
    "courage": Spell("courage", 5, 1, "DEF", inf, 0, -1, True,[], []),
    "doublecut": Spell("doublecut", 5, 2, "STR", "DEX", 1.25, 0, False, [ ], [ ]),
    "bolt": Spell("bolt", 5, 1, "MP", "AGI", .5, 0, False, [], []),
    "fireball": Spell("fireball", 15, 1, "MP", "DEF", 3, .25, False, ["burning"], ["burning"]),
    "nuke": Spell("nuke", 0, 10, "HP", inf, 99999, 0, True, [], [])
}

monsters = {
    "rat": Entity("rat", 3, inf, 1, 0, 0, 0, [], []),
    "wolf": Entity("wolf", 10, inf, 2, 3, 1, 0, [], []),
    "imp": Entity("imp", 15, inf, 4, 5, -3, 0, ["bolt"], []),
}

def calcHit(victimAGI: int, attackerDEX: int):
    # roll for agi proc. if fail, hit
    if (victimAGI < 1): victimAGI = 1
    if (attackerDEX < 1): attackerDEX = 1
    if (victimAGI == 3): 
        hitChance = round(log(((attackerDEX) * (2.999999 / (victimAGI + 0.0000001)))) * 40) + 55
    else: 
        hitChance = round(log((attackerDEX) * (3 / (victimAGI + 0.0000001))) * 40) + 45
    if (hitChance < 30): hitChance = 30
    if (hitChance >= randint(1,100)): return True
    else: return False

# self, mana cost, number of casts, stat to use, power of attack (multiplier), stat for hit, damage take on cast (multiplier), effects to enemy, effects to caster
def castSpell(spell, caster, victim):
    print("")
    spell = spells[spell]
    if (caster.name != "you"):
        if (spell.name == "attack"):
            print("the " + caster.name + " attacks")
        else:
            print("the " + caster.name + " casts " + spell.name + "!")
    else:
        if (spell.name == "attack"):
            print(caster.name + " attack")
        else:
            print(caster.name + " cast " + spell.name + "!")
    if (spell.hitStat == inf): bypassHit = True
    else: bypassHit = False
    for each in range(spell.procs):
        if (bypassHit or calcHit(eval("caster." + str(spell.hitStat)), victim.AGI)):
            if (spell.ignoreEnemy == False):
                damage = round((eval("caster." + str(spell.dmgStat)) * spell.damage * (randint(90, 110)/100)) - victim.DEF)
            else:
                damage = round((eval("caster." + str(spell.dmgStat)) * (randint(90, 110)/100)))
            if (damage <= 0):
                print("0 damage")
            else:
                print(str(damage) + " damage")
                victim.HP -= damage
            casterDamage = damage * spell.damageRecoil
            if (casterDamage != 0):
                if (caster.name == "you"):
                    if (casterDamage < 0):
                        print("you healed " + str(casterDamage * -1) + " hp")
                    else:
                        print("you took " + str(casterDamage) + " damage from recoil")
                else:
                    if (casterDamage < 0):
                        print("the " + caster.name + " healed " + str(casterDamage * -1) + " hp")
                    else:
                        print("the " + caster.name + " took " + str(casterDamage) + " damage from recoil")
                caster.HP -= casterDamage
        else:
            print("miss")
    print("")
    if (victim.HP < 0): victim.HP = 0
    if (caster.name != "you"): print("your hp: " + str(victim.HP) + " / " + str(victim.MaxHP))
    else: print(victim.name + " hp: " + str(victim.HP) + " / " + str(victim.MaxHP))

def verify(question:str=None, allowed:list=None):
    index = 0
    for prompt in allowed:
        allowed[index] = prompt.lower()
        index += 1
    del index
    if (allowed == None):
        print("no given list for verify, returned statement")
        return
    if (question == None):
        question = "what will you do? "
    while (True):
        chosen = input(question)
        chosen = chosen.lower()
        for i in allowed:
            i = i.lower()
            if (chosen == i):
                return chosen

def doCombat(player, enemy):
    enemy = copy(monsters[enemy])
    print("an " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your mana: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = verify("what would you like to do? [attack, spell, item] ", ["attack", "spell", "skill", "item", "a", "s", "i"])
        if (chosen == "attack" or chosen == "a"):
            castSpell("attack", player, enemy)
        elif (chosen == "spell" or chosen == "skill" or chosen == "s"):
            print("")
            print("your spells:")
            for each in player.spells:
                each = spells[each]
                print(each.name + ": " + str(each.cost) + " MP")
            print("")
            allowed = player.spells + ["back"]
            chosen = verify("choose an skill to use, or type back to go back: ", allowed)
            if (chosen == "back"):
                continue
            else:
                if (spells[chosen].cost <= player.MP):
                    castSpell(chosen, player, enemy)
                    spells[chosen].cost
                else:
                    print("not enough mana!")
                    print("")
                    continue
        elif (chosen == "item" or chosen == "i"):
            print("WHAT THE HELL IS AN ITEM *eagle screech*")
            continue
        if (enemy.HP > 0):
            castSpell(enemy.skillSelect(enemy.spells), enemy, player)
    if (player.HP > 0):
        print("victory!")
        print("level up!")
        chosen = verify("pick a stat to increase [HP, MP, STR, DEX, DEF, AGI]: ", ["HP", "MP", "STR", "DEX", "DEF", "AGI"])
        chosen = chosen.upper()
        if (chosen == "HP"):
            player.MaxHP += 5
            player.HP = player.MaxHP
            print("HP increased by 5.")
            print("HP fully restored.")
        elif (chosen == "MP"):
            player.MaxMP += 2
            player.MP = player.MaxMP
            print("MP increased by 2.")
            print("MP fully restored.")
        else:
            exec("player." + chosen + " += 2")
            print(chosen + " increased by 2.")
        print("")
    else:
        print("you were slain...")
        quit()

player = Entity("you", 10, 5, 3, 3, 0, 0, ["courage", "doublecut", "nuke"], [])

doCombat(player, "wolf")

doCombat(player, "wolf")