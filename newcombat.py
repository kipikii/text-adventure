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
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damage: float, damageRecoil: float, ignoreEnemyDEF: bool, victimEffect: str, selfEffect: str):
        # spell's name
        self.name = name
        # spell's MP cost
        self.cost = cost
        # spell's damage multiplier
        self.damage = damage
        # number of times the spell hits
        self.procs = procs
        # the stat that the spell will use to calculate damage
        self.dmgStat = dmgStat
        # the stat that the spell will use to calculate hit chance
        self.hitStat = hitStat
        # multiplier of the damage that the player will take when compared to you the damage you deal
        self.damageRecoil = damageRecoil
        # if the attack should ignore the enemy's defense when calculating damage
        self.ignoreEnemyDEF = ignoreEnemyDEF
        # code to execute if the victim was hit by the spell
        self.victimEffect = victimEffect
        # code to execute after casting the spell (regardless of hitting)
        self.selfEffect = selfEffect

class Equipment:
    def __init__(self, slot: str, BonusHP: int, BonusMP: int, BonusSTR: int, BonusDEX: int, BonusDEF: int, BonusAGI: int, onTurnStart: list, onAttack: list, onCast: list, onHit: list, onHurt: list):
        self.slot = slot
        self.HP = BonusHP
        self.MP = BonusMP
        self.STR = BonusSTR
        self.DEX = BonusDEX
        self.DEF = BonusDEF
        self.AGI = BonusAGI
        
        self.onTurnStart = onTurnStart
        self.onAttack = onAttack
        self.onCast = onCast
        self.onHit = onHit
        self.onHurt = onHurt

class Entity:
    def __init__(self, name: str, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list, inventory: dict, blessings: list, onTurnStart: list = [], onAttack: list = [], onCast: list = [], onHit: list = [], onHurt: list = []):
        self.level = 1
        # experience points
        self.XP = 0
        self.MaxXP = 10
        # entity's name ("you" if player)
        self.name = name
        # health points
        self.HP = HP
        self.MaxHP = HP
        # mana points
        self.MP = MP
        self.MaxMP = MP
        # strength, dexterity, defense, agility
        self.STR = STR
        self.DEX = DEX
        self.DEF = DEF
        self.AGI = AGI
        # spells the entity has
        self.spells = spells
        # status effects currently applied to the entity
        self.status = [ ]
        # passive effects
        self.blessings = blessings
        # items held by the entity
        self.inventory = inventory
        # equipped items
        self.equip = {
            "weapon": None,
            "head": None,
            "chest": None,
            "legs": None,
            "charm": None
        }
        # combat conditionals, default blank, all will be exec()'d
        self.onTurnStart = onTurnStart
        self.onAttack = onAttack
            # for enemies, onCast is NEVER used, use onAttack instead
        self.onCast = onCast
            # note: onHit and onHurt are executed in castSpell, when about the other target use "victim" and for self, use "caster"
        self.onHit = onHit
        self.onHurt = onHurt

class Status:
    def __init__(self, name: str, fadeChance: float, affectOnApply: bool, effect: str, reverseEffect: str):
        # status effect's name
        self.name = name
        # chance for the status effect to disappear from the entity at the end of their turn
        self.fadeChance = fadeChance
        # if the status should proc when applied, and nothing afterwards
        self.affectOnApply = affectOnApply 
        self.effect = effect # to be exec()'d
        self.reverseEffect = reverseEffect  # to be exec()'d

spells = {
    # melee attacks
    "attack": Spell("attack", 0, 1, "STR", "DEX", 1, 0, False, "pass", "pass"),
    "doublecut": Spell("doublecut", 5, 2, "STR", "DEX", 2, 0, False, "pass", "pass"),
    "tricut": Spell("tricut", 8, 3, "STR", "DEX", 3, 0, False, "pass", "pass"),
    "bite": Spell("bite", 2, 1, "STR", "DEX", 1, 0, False, "applyStatus('poison', victim)", "pass"),
    
    # spells
    "bolt": Spell("bolt", 5, 1, "MP", "AGI", .75, 0, False, "pass", "pass"),
    "flame": Spell("flame", 5, 1, "AGI", "DEX", 1, 0, False, "applyStatus('burn', victim)", "pass"),
    "fireball": Spell("fireball", 15, 1, "MP", "DEX", 3, .25, False, "applyStatus('burn', victim)", "applyStatus('burn', caster)"),
    "nuke": Spell("nuke", 100784, 999, "HP", inf, 99999, 0, True, "pass", "pass"),
    "doom": Spell("doom", 100, 1, "AGI", inf, 0, 0, False, "applyStatus('impending doom', victim)", "pass"),

    # buffs
    "warcry": Spell("warcry", 10, 1, "STR", inf, 0, 0, True, "pass", "applyStatus('STR up', caster)"),
    "foresee": Spell("foresee", 10, 1, "DEX", inf, 0, 0, True, "pass", "applyStatus('DEX up', caster)"),
    "protection": Spell("protection", 10, 1, "DEF", inf, 0, 0, True, "pass", "applyStatus('DEF up', caster)"),
    "evasion": Spell("evasion", 10, 1, "AGI", inf, 0, 0, True, "pass", "applyStatus('AGI up', caster)"),
    "bunny": Spell("bunny", 50, 1, "AGI", inf, 0, 0, True, "applyStatus('bunnied', victim)", "applyStatus('bunny', caster)"),

    # debuffs
    "threaten": Spell("threaten", 10, 1, "STR", inf, 0, 0, True, "applyStatus('STR down', victim)", "pass"),
    "trip": Spell("trip", 10, 1, "DEX", inf, 0, 0, True, "applyStatus('DEX down', victim)", "pass"),
    "exploit": Spell("exploit", 10, 1, "DEF", inf, 0, 0, True, "applyStatus('DEF down', victim)", "pass"),
    "slow": Spell("slow", 10, 1, "AGI", inf, 0, 0, True, "applyStatus('AGI down', victim)", "pass"),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "DEF", inf, 0, -1, True, "pass", "pass"),
    "courage": Spell("courage", 15, 2, "DEF", inf, 0, -1.2, True, "pass", "pass"),
    "valor": Spell("valor", 45, 3, "DEF", inf, 0, -1.8, True, "pass", "if(randint(1,4) == 1): applyStatus('DEF up', caster)"),

    # items

}

statuses = {
    # stat buffs
    "STR up": Status("STR up", 0, True, "victim.STR *= 6/5", "victim.STR /= 6/5"),
    "DEX up": Status("DEX up", 0, True, "victim.DEX *= 6/5", "victim.DEX /= 6/5"),
    "DEF up": Status("DEF up", 0, True, "victim.DEF *= 6/5", "victim.DEF /= 6/5"),
    "AGI up": Status("AGI up", 0, True, "victim.AGI *= 6/5", "victim.AGI /= 6/5"),
    "bunny": Status("bunny", .10, True, "victim.AGI *= 4\nvictim.STR /= 8", "victim.AGI /= 4\nvictim.STR *= 8"),

    # stat debuffs
    "STR down": Status("STR down", 0, True, "victim.STR /= 6/5", "victim.STR *= 6/5"),
    "DEX down": Status("DEX down", 0, True, "victim.DEX /= 6/5", "victim.DEX *= 6/5"),
    "DEF down": Status("DEF down", 0, True, "victim.DEF /= 6/5", "victim.DEF *= 6/5"),
    "AGI down": Status("AGI down", 0, True, "victim.AGI /= 6/5", "victim.AGI *= 6/5"),
    "bunnied": Status("bunnied", .10, True, "victim.DEX /= 4\nvictim.STR /= 4", "victim.DEX *= 4\nvictim.STR *= 4"),

    # DOT effects
    "burn": Status("burn", .25, False, """
burndmg = ceil(victim.MaxHP / 20)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from burn')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from burn')
victim.HP -= burndmg
del burndmg""", "pass"),

    "poison": Status("poison", .1, False, """
burndmg = ceil(victim.MaxHP / 20)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from poison')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from poison')
victim.HP -= burndmg
del burndmg""", "pass"),

    # other
    "impending doom": Status("impending doom", .33, False, "pass", "applyStatus('doom', victim)"),
    "doom": Status("doom", 0, False, "print('death calls.')\nprint('your HP drops to 0')\nvictim.HP = 0", "pass"),
}

monsters = {
    # forest
    "rat": Entity("rat", 3, inf, 1, 0, 0, 0, ["bite"], {}, []),
    "wolf": Entity("wolf", 15, inf, 2, 3, 1, 1, ["attack"], {}, []),
    "spirit": Entity("spirit", 25, inf, 4, 5, 0, 4, ["attack", "flame"], {}, []),

    # infernal wastes
    "imp": Entity('imp', 70, inf, 10, 15, -5, 20, ["evasion", "attack", "flame", "threaten"], {}, []),
    "demon": Entity('demon', 100, inf, 25, 10, 6, 10, ["attack", "flame", "courage", "warcry", "foresee"], {}, []),
    "warg": Entity('warg', 150, inf, 10, 20, 10, 10, ["bite", "tricut"], {}, [], ["applyStatus('STR up', enemy)"]),

    # what the hell
    "reaper": Entity("reaper", 666, inf, 100, 200, 50, 100, ["doom", "bunny", "evasion", "trip"], {}, [])
}

# calculates if an attack should hit a given entity
def calcHit(victimAGI: int, attackerDEX: int):
    if (victimAGI < 1): victimAGI = 1
    if (attackerDEX < 1): attackerDEX = 1
    if (victimAGI == 3): 
        hitChance = round(log(attackerDEX * (2.999999 / (victimAGI + 0.0000001))) * 40  ) + 90
    else: 
        hitChance = round(log((attackerDEX) * (3 / (victimAGI + 0.0000001))) * 40) + 90
    if (hitChance < 30): hitChance = 30
    if (hitChance >= randint(1,100)): return True
    else: return False

# gives a status effect to an entity
def applyStatus(status: str, victim:object):
    status = copy(statuses[status])
    if (victim.name == "you"):
        print("you now have " + status.name)
    else:
        print(victim.name + " now has " + status.name)
    victim.status += [status.name]
    if (status.affectOnApply):
        exec(status.effect)

# removes a status effect from an entity
def removeStatus(status: str, victim:object):
    if (status.name in victim.status):
        victim.status.remove(status.name)
        if (victim.name == "you"):
            print("you no longer have " + status.name)
        else:
            print(status.name + " faded from the " + victim.name)

# causes a status effect to execute it's effect
def tickStatus(status: str, victim:object):
    status = copy(statuses[status])
    if (status.affectOnApply == False):
        exec(status.effect)
        if (status.fadeChance >= uniform(0,1)):
            removeStatus(status, victim)

# mana cost, number of casts, stat to use, power of attack (multiplier), stat for hit, damage take on cast (multiplier), effects to enemy, effects to caster
def castSpell(spell:object, caster:object, victim:object):
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
        for each in caster.onHit:
            exec(each)
        for each in victim.onHit:
            exec(each)
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

# provided a list and a question, forces the player to make a choice from the list
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
        if (chosen.startswith("/")):
            if (chosen == "/help"):
                print("/help - displays this menu")
                print("/stats - displays your current stats")
                print("/quit - quits the game")
                print("/patchnotes - shows the patch notes")
            elif (chosen == "/stats"):
                global player
                print("")
                print("~~~~~~~~~~")
                print("level: " + str(player.level))
                print("XP: " + str(player.XP) + "/" + str(player.MaxXP))
                print("")
                print("HP: " + str(player.HP) + "/" + str(player.MaxHP))
                print("MP: " + str(player.MP) + "/" + str(player.MaxMP))
                print("")
                print("STR: " + str (player.STR))
                print("DEX: " + str (player.DEX))
                print("DEF: " + str (player.DEF))
                print("AGI: " + str (player.AGI))
                print("~~~~~~~~~~")
                print("")
            elif (chosen == "/patchnotes"):
                raise ValueError('Variable "patchnotes" is too long to print. Try separating the variable into two different print statements.')
            elif (chosen == "/quit"):
                print("bye!")
                quit()
            else:
                print("invalid command. to see all valid commands, do /help")
        for i in allowed:
            i = i.lower()
            if (chosen == i):
                return chosen

def equipItem(equipper:object, armor:object, slot:str):
    equipper.equip[slot] = armor

    equipper.MaxHP += armor.HP
    equipper.MaxMP += armor.MP
    equipper.STR += armor.STR
    equipper.DEX += armor.DEX
    equipper.DEF += armor.DEF
    equipper.DEF += armor.AGI

    equipper.onTurnStart += armor.onTurnStart
    equipper.onAttack += armor.onAttack
    equipper.onCast += armor.onCast
    equipper.onHit += armor.onHit
    equipper.onHurt += armor.onHurt

def unequipItem(equipper:object, slot:str):
    armor = equipper.equip[slot]

    equipper.MaxHP -= armor.HP
    if equipper.HP > equipper.maxHP: equipper.HP = equipper.MaxHP
    equipper.MaxMP -= armor.MP
    if equipper.MP > equipper.maxMP: equipper.MP = equipper.MaxMP
    equipper.STR -= armor.STR
    equipper.DEX -= armor.DEX
    equipper.DEF -= armor.DEF
    equipper.DEF -= armor.AGI

    for code in armor.onTurnStart:
        equipper.onTurnStart.remove(code)
    for code in armor.onAttack:
        equipper.onAttack.remove(code)
    for code in armor.onTurnStart:
        equipper.onCast.remove(code)
    for code in armor.onHit:
        equipper.onHit.remove(code)
    for code in armor.onHurt:
        equipper.onHurt.remove(code)

def generateEquip():
    pass

# causes a combat to initate between two entities
def doCombat(player: object, enemy: object):
    enemy = copy(monsters[enemy])
    print("a " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        for each in player.onTurnStart:
            exec(each)
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your MP: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = verify("what would you like to do? [attack, spell, item]\n> ", ["attack", "spell", "skill", "item", "a", "s", "i"])
        if (chosen == "attack" or chosen == "a"):
            clearTerminal()
            castSpell("attack", player, enemy)
            for each in player.onHit:
                exec(each)
        elif (chosen == "spell" or chosen == "skill" or chosen == "s"):
            print("")
            print("your spells:")
            for each in player.spells:
                each = spells[each]
                print(each.name + ": " + str(each.cost) + " MP")
            print("")
            allowed = player.spells + ["back"]
            chosen = verify("choose an skill to use, or type back to go back\n> ", allowed)
            if (chosen == "back"):
                clearTerminal()
                continue
            else:
                clearTerminal()
                if (spells[chosen].cost <= player.MP):
                    castSpell(chosen, player, enemy)
                    for each in player.onCast:
                        exec(each)
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
            for each in enemy.onTurnStart:
                exec(each)
            print("")
            castSpell(choice(enemy.spells), enemy, player)
            for each in enemy.onAttack:
                exec(each)
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
            chosen = verify("pick a stat to increase [HP, MP, STR, DEX, DEF, AGI]\n> ", ["HP", "MP", "STR", "DEX", "DEF", "AGI"])
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
        end = None
        while (end != "quit"):
            end = input("type 'quit' to quit the app\n> ")
            clearTerminal()
        quit()

# allows the player to heal, equip gear
def restSite(player: object):
    randchoice = choice(["campfire", "campsite", "clearing", "small ruin"])
    print("you come across a " + randchoice)
    print("you feel like this is a safe place for you to gather yourself.")
    print("")
    chosen = None
    while (True):
        chosen = verify("what will you do? [rest, equip, leave]\n> ", ["rest", "equip", "leave", "r", "e", "l"])
        if (chosen == "rest" or chosen == "r"):
            if (player.HP >= player.MaxHP and player.MP >= player.MaxMP):
                print("you already feel rested, no reason to do so")
                input("enter anything to continue...\n> ")
                clearTerminal()
            else:
                player.HP = player.MaxHP
                player.MP = player.MaxMP
                print("MP and HP fully restored!")
                input("enter anything to continue...\n> ")
                clearTerminal()
        elif (chosen == "equip" or chosen == "e"):
            print("you're not even sure what equipping means, so you decide not to do that, whatever it means.")   
            input("enter anything to continue... ")
            clearTerminal()
        elif (chosen == "leave" or chosen == "l"):
            print("")
            input("enter anything to continue...\n> ")
            clearTerminal()
            break

player = Entity("you", 20, 5, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery"], { }, [], ["print('turn started')"], ["print('attacked enemy')"], ["print('casted a spell')"], ["print('hit enemy')"], ["print('got hurt')"])

doCombat(player, "rat")
doCombat(player, "wolf")
doCombat(player, "wolf")
restSite(player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!")
player.spells += ["bite"]
print("")
input("enter anything to continue...\n> ")
clearTerminal()
doCombat(player, "spirit")
doCombat(player, "spirit")
doCombat(player, "imp")
doCombat(player, "imp")
doCombat(player, "demon")
restSite(player)
print("your experience with fighting spirits and demons have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
player.spells += ["flame", "fireball"]
print("")
input("enter anything to continue...\n> ")
clearTerminal()
doCombat(player, "warg")
restSite(player)
doCombat(player, "reaper")
print("wowie.")
