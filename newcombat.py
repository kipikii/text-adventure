### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
from random import *    
from math import *
from time import *
from copy import *
import os

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clearTerminal()

class Spell:
    # self, mana cost, number of casts, stat to use, power of attack (multiplier), stat for hit, damage take on cast (multiplier), effects to enemy, effects to caster, ignore enemy defense
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damage: float, damageRecoil: float, ignoreEnemyDEF: bool, victimEffect: str, selfEffect: str):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.procs = procs
        self.dmgStat = dmgStat
        self.hitStat = hitStat
        self.damageRecoil = damageRecoil
        self.ignoreEnemyDEF = ignoreEnemyDEF
        self.victimEffect = victimEffect
        self.selfEffect = selfEffect

class Equipment:
    def __init__(self, slot: str, BonusHP: int, BonusMP: int, BonusSTR: int, BonusDEX: int, BonusDEF: int, BonusAGI: int, onTurnStart: str, onAttack: str, onHit: str, onHurt: str, onStatusGain: str, onApplyStatus: str):
        self.slot = slot
        self.BonusHP = BonusHP
        self.BonusMP = BonusMP
        self.BonusSTR = BonusSTR
        self.BonusDEX = BonusDEX
        self.BonusDEF = BonusDEF
        self.BonusAGI = BonusAGI

class Entity:
    def __init__(self, name, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list, inventory: dict, blessings: list):
        self.level = 1
        self.XP = 0
        self.MaxXP = 10
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

class Status:
    def __init__(self, name: str, fadeChance: float, affectChance: float, affectOnApply: bool, effect: str, reverseEffect: str):
        self.name = name
        self.fadeChance = fadeChance
        self.affectChance = affectChance
        self.affectOnApply = affectOnApply
        self.effect = effect # to be exec()'d!
        self.reverseEffect = reverseEffect  # also to be exec()'d!

spells = {
    # melee attacks
    "attack": Spell("attack", 0, 1, "STR", "DEX", 1, 0, False, "pass", "pass"),
    "doublecut": Spell("doublecut", 5, 2, "STR", "DEX", 2, 0, False, "pass", "pass"),
    "tricut": Spell("tricut", 8, 3, "STR", "DEX", 3, 0, False, "pass", "pass"),
    "bite": Spell("bite", 2, 1, "STR", "DEX", 1, 0, False, "applyStatus('poison', victim)", "pass"),
    
    # spells
    "bolt": Spell("bolt", 5, 1, "MP", "AGI", .5, 0, False, "pass", "pass"),
    "flame": Spell("flame", 5, 1, "AGI", "DEX", 1, 0, False, "applyStatus('burn', victim)", "pass"),
    "fireball": Spell("fireball", 15, 1, "MP", "DEF", 3, .25, False, "applyStatus('burn', victim)", "applyStatus('burn', caster)"),
    "nuke": Spell("nuke", 100784, 10, "HP", inf, 99999, 0, True, "pass", "pass"),
    "doom": Spell("doom", 100, 1, "AGI", inf, 0, 0, False, "applyStatus('impending doom (3)', victim)", "pass"),

    # buffs
    "warcry": Spell("warcry", 10, 1, "STR", inf, 0, 0, True, "pass", "applyStatus('STR up', caster)"),
    "foresee": Spell("foresee", 10, 1, "DEX", inf, 0, 0, True, "pass", "applyStatus('DEX up', caster)"),
    "protection": Spell("protection", 10, 1, "DEF", inf, 0, 0, True, "pass", "applyStatus('DEF up', caster)"),
    "evasion": Spell("evasion", 10, 1, "AGI", inf, 0, 0, True, "pass", "applyStatus('AGI up', caster)"),
    "bunny": Spell("bunny", 50, 1, "AGI", inf, 0, 0, True, "applyStatus('bunnied', victim)", "applyStatus('bunny', caster)"),

    # debuffs
    "threaten": Spell("threaten", 10, 1, "STR", inf, 0, 0, True, "applyStatus('STR down', victim)", "pass"),
    "trip": Spell("trip", 10, 1, "DEX", inf, 0, 0, True, "applyStatus('DEX down', victim)", "pass"),
    "exploit": Spell("exploit", 10, 1, "DEF", inf, 0, 0, True, "applyStatus('DEX down', victim)", "pass"),
    "slow": Spell("slow", 10, 1, "AGI", inf, 0, 0, True, "applyStatus('DEX down', victim)", "pass"),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "DEF", inf, 0, -1, True, "pass", "pass"),
    "courage": Spell("courage", 15, 2, "DEF", inf, 0, -1.2, True, "pass", "pass"),
    "valor": Spell("valor", 45, 3, "DEF", inf, 0, -1.8, True, "pass", "if(random.randint(1,4) == 1): applyStatus('DEF up', caster)"),
}

statuses = {
    "STR up": Status("STR up", 0, 0, True, "victim.STR /= 7/8", "victim.STR *= 7/8"),
    "DEX up": Status("DEX up", 0, 0, True, "victim.DEX /= 7/8", "victim.DEX *= 7/8"),
    "DEF up": Status("DEF up", 0, 0, True, "victim.DEF /= 7/8", "victim.DEF *= 7/8"),
    "AGI up": Status("AGI up", 0, 0, True, "victim.AGI /= 7/8", "victim.AGI *= 7/8"),
    "STR down": Status("STR down", 0, 0, True, "victim.STR *= 7/8", "victim.STR /= 7/8"),
    "DEX down": Status("DEX down", 0, 0, True, "victim.DEX *= 7/8", "victim.DEX /= 7/8"),
    "DEF down": Status("DEF down", 0, 0, True, "victim.DEF *= 7/8", "victim.DEF /= 7/8"),
    "AGI down": Status("AGI down", 0, 0, True, "victim.AGI *= 7/8", "victim.AGI /= 7/8"),

    "burn": Status("burn", .25, 1, False, """
burndmg = ceil(victim.MaxHP / 20)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from burn')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from burn')
victim.HP -= burndmg
del burndmg""", "pass"),

    "poison": Status("poison", .1, .75, False, """
burndmg = ceil(victim.MaxHP / 20)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from poison')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from poison')
victim.HP -= burndmg
del burndmg""", "pass"),

    "impending doom (3)": Status("impending doom (3)", 1, 1, False, "applyStatus('impending doom (2)', victim)", "pass"),
    "impending doom (2)": Status("impending doom (2)", 1, 1, False, "applyStatus('impending doom (1)', victim)", "pass"),
    "impending doom (1)": Status("impending doom (1)", 1, 1, False, "applyStatus('doom', victim)", "pass"),
    "doom": Status("doom", 0, 1, False, "print('death calls.')\nprint('your HP drops to 0')\nvictim.HP = 0", "pass"),
    "bunny": Status("bunny", .10, 0, True, "victim.AGI *= 4\nvictim.STR /= 8", "victim.AGI /= 4\nvictim.STR *= 8"),
    "bunnied": Status("bunnied", .10, 0, True, "victim.DEX /= 4\nvictim.STR /= 4", "victim.DEX *= 4\nvictim.STR *= 4")
}

monsters = {
    # forest
    "rat": Entity("rat", 3, inf, 1, 0, 0, 0, ["bite"], {}, []),
    "wolf": Entity("wolf", 15, inf, 2, 3, 1, 1, ["attack"], {}, []),
    "spirit": Entity("spirit", 25, inf, 4, 5, 0, 4, ["attack", "flame"], {}, []),

    # infernal wastes
    "imp": Entity('imp', 70, inf, 10, 15, -5, 20, ["evasion", "attack", "flame", "threaten"], {}, []),

    # what the hell
    "reaper": Entity("reaper", 666, inf, 100, 200, 50, 100, ["doom", "bunny", "evasion", "trip"], {}, [])
}

def skillSelect(skills: list):
    toUse = skills[randint(0, (len(skills)-1))]
    return toUse

def calcHit(victimAGI: int, attackerDEX: int):
    # roll for agi proc. if fail, hit
    if (victimAGI < 1): victimAGI = 1
    if (attackerDEX < 1): attackerDEX = 1
    if (victimAGI == 3): 
        hitChance = round(log(attackerDEX * (2.999999 / (victimAGI + 0.0000001))) * 40  ) + 90
    else: 
        hitChance = round(log((attackerDEX) * (3 / (victimAGI + 0.0000001))) * 40) + 90
    if (hitChance < 30): hitChance = 30
    if (hitChance >= randint(1,100)): return True
    else: return False

def applyStatus(status: str, victim):
    status = copy(statuses[status])
    if (status.name in victim.status):
        return
    if (victim.name == "you"):
        print("you now have " + status.name)
    else:
        print(victim.name + " now has " + status.name)
    victim.status += [status.name]
    if (status.affectOnApply):
        exec(status.effect)

def removeStatus(status: str, victim):
    if (status.name in victim.status):
        victim.status.remove(status.name)
        if (victim.name == "you"):
            print("you no longer have " + status.name)
        else:
            print(status.name + " faded from the " + victim.name)

def tickStatus(status: str, victim):
    status = copy(statuses[status])
    if (status.affectOnApply == False):
        if (status.affectChance >= uniform(0,1)):
            exec(status.effect)
        if (status.fadeChance >= uniform(0,1)):
            removeStatus(status, victim)

# self, mana cost, number of casts, stat to use, power of attack (multiplier), stat for hit, damage take on cast (multiplier), effects to enemy, effects to caster
def castSpell(spell, caster, victim):
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
    spellHit = False
    for each in range(spell.procs):
        if (bypassHit or calcHit(eval("caster." + str(spell.hitStat)), victim.AGI)):
            spellHit = True
            if (spell.ignoreEnemyDEF == False):
                damage = ceil((eval("caster." + str(spell.dmgStat)) * (randint(90, 110)/100)) - victim.DEF)
            else:
                damage = ceil((eval("caster." + str(spell.dmgStat)) * (randint(90, 110)/100)))
            if (damage <= 0):
                if (spell.damage != 0):
                    print("0 damage")
            else:
                if (spell.damage != 0):
                    print(str(ceil(damage * spell.damage)) + " damage")
                    victim.HP -= ceil(damage * spell.damage)
        else:
            print("miss")
            damage = 0
        casterDamage = damage * spell.damageRecoil
        if (casterDamage != 0):
            casterDamage = ceil(casterDamage)
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
            if (caster.HP > caster.MaxHP): caster.HP = caster.MaxHP
    if (spellHit):
        exec(spell.victimEffect)
    exec(spell.selfEffect)
    print("")
    caster.MP -= spell.cost
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

def makeEquip(slot, equipper):
    pass

def doCombat(player, enemy):
    enemy = copy(monsters[enemy])
    print("a " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your MP: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = verify("what would you like to do? [attack, spell, item] ", ["attack", "spell", "skill", "item", "a", "s", "i"])
        if (chosen == "attack" or chosen == "a"):
            clearTerminal()
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
                clearTerminal()
                continue
            else:
                clearTerminal()
                if (spells[chosen].cost <= player.MP):
                    castSpell(chosen, player, enemy)
                    spells[chosen].cost
                else:
                    clearTerminal()
                    print("not enough mana!")
                    print("")
                    continue
        elif (chosen == "item" or chosen == "i"):
            print("WHAT THE HELL IS AN ITEM *eagle screech*")
            continue
        for each in player.status:
            tickStatus(each, player)
        player.MP += ceil(player.MaxMP / 10)
        if (player.MP > player.MaxMP): player.MP = player.MaxMP
        if (enemy.HP > 0):
            print("")
            castSpell(skillSelect(enemy.spells), enemy, player)
            for each in enemy.status:
                tickStatus(each, enemy)
    if (player.HP > 0):
        for each in player.status:
            each = copy(statuses[each])
            removeStatus(each, player)
        print("")
        print("victory!")
        xpGain = round(enemy.MaxHP * uniform(1, 1.4)) + randint(0, 3)
        print("you gained " + str(xpGain) + " xp")
        player.XP += xpGain
        del xpGain
        while (player.XP >= player.MaxXP):
            print("")
            print("*** level up! ***")
            print("Max HP increased by 5, max MP increased by 2, and all stats increased by 1!")
            player.MaxHP += 5
            player.MaxMP += 2
            player.STR += 1
            player.DEX += 1
            player.DEF += 1
            player.AGI += 1
            chosen = verify("pick a stat to increase [HP, MP, STR, DEX, DEF, AGI]: ", ["HP", "MP", "STR", "DEX", "DEF", "AGI"])
            chosen = chosen.upper()
            if (chosen == "HP"):
                player.MaxHP += 3
                player.HP = player.MaxHP
                print("Max HP increased by 3")
                print("HP fully restored!")
            elif (chosen == "MP"):
                player.MaxMP += 1
                player.MP = player.MaxMP
                print("Max MP increased by 2")
                print("MP fully restored!")
            else:
                exec("player." + chosen + " += 1")
                print(chosen + " increased by 1")
            player.XP -= player.MaxXP
            player.MaxXP = round(player.MaxXP * 1.5)
            player.level += 1
        print("")
        input("enter anything to continue... ")
        clearTerminal()
    else:
        print("you were slain...")
        quit()

def restSite(player):
    randchoice = choice(["campfire", "campsite", "clearing", "small ruin"])
    print("you come across a " + randchoice)
    print("you feel like this is a safe place for you to gather yourself.")
    print("")
    chosen = None
    while (chosen != "leave"):
        chosen = verify("what will you do? [rest, equip, leave] ", ["rest", "equip", "leave"])
        if (chosen == "rest"):
            player.HP = player.MaxHP
            player.MP = player.MaxMP
            print("MP and HP fully restored!")
            input("enter anything to continue... ")
            clearTerminal()
        elif (chosen == "equip"):
            print("you're not even sure what equipping means, so you decide not to do that, whatever it means.")   
            input("enter anything to continue... ")
            clearTerminal()
        elif (chosen == "leave"):
            print("time to get back on the road.")
            input("enter anything to continue... ")
            clearTerminal()

player = Entity("you", 20, 5, 3, 5, 0, 0, ["doublecut", "warcry", "protection", "bravery"], { }, [])

doCombat(player, "rat")
doCombat(player, "wolf")
doCombat(player, "wolf")
restSite(player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!")
player.spells += ["bite"]
print("")
input("enter anything to continue... ")
clearTerminal()
doCombat(player, "spirit")
doCombat(player, "spirit")
doCombat(player, "imp")
doCombat(player, "imp")
restSite(player)
print("your experience with fighting spirits and imps have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
player.spells += ["flame", "fireball"]
print("")
input("enter anything to continue... ")
clearTerminal()
doCombat(player, "reaper")