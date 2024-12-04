### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
from random import *    
from math import *
from time import *
from copy import *
import os

armor_adjectives = [
    "durable",
    "sturdy",
    "resilient",
    "heavy",
    "lightweight",
    "reinforced",
    "imposing",
    "gleaming",
    "shiny",
    "polished",
    "ornate",
    "simple",
    "intricate",
    "decorative",
    "protective",
    "indestructible",
    "formidable",
    "battle-worn",
    "spiked",
    "hardened",
    "plate",
    "leather",
    "flexible",
    "heavy-duty",
    "glimmering",
    "enchanted",
    "runic",
    "sacred",
    "ethereal",
    "resistant",
    "insulated",
    "thick",
    "layered",
    "armored",
    "reinforced",
    "fortified",
    "resplendent",
    "tough",
    "sleek",
    "metallic",
    "riveted",
    "chiseled",
    "scarred",
    "adaptable",
    "immaculate",
    "battle-ready",
    "weathered",
    "custom",
    "magicked",
    "ancient",
    "mythic",
    "unyielding",
    "combat-ready",
    "heavy-duty",
    "sharp-edged",
    "bladed",
    "scaled",
    "enigmatic",
    "fireproof",
    "shockproof",
    "cute",
    "repaired"
]

def clearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clearTerminal()

class Spell:
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damageRecoil: float, ignoreEnemyDEF: bool, victimEffect: str, selfEffect: str):
        # spell's name
        self.name = name
        # spell's MP cost
        self.cost = cost
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
    def __init__(self, name:str, slot: str, BonusHP: int, BonusMP: int, BonusSTR: int, BonusDEX: int, BonusDEF: int, BonusAGI: int, onTurnStart: list, onAttack: list, onCast: list, onHit: list, onHurt: list):
        self.name = name
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
    def __init__(self, name: str, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list,
     inventory: dict, blessings: list, onTurnStart: list = [], onAttack: list = [], onCast: list = [], 
     onHit: list = [], onHurt: list = []
     ):
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
        # armor held by the entity
        self.heldarmors = {}
        # equipped items
        self.equip = {
            "weapon": None,
            "helmet": None,
            "chestplate": None,
            "boots": None,
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
    "attack": Spell("attack", 0, 1, "caster.STR", "caster.DEX", 0, False, "pass", "pass"),
    "doublecut": Spell("doublecut", 5, 2, "caster.STR * 2", "caster.DEX", 0, False, "pass", "pass"),
    "tricut": Spell("tricut", 8, 3, "caster.STR * 3", "caster.DEX", 0, False, "pass", "pass"),
    "bite": Spell("bite", 2, 1, "caster.STR", "caster.STR", 0, False, "applyStatus('poison', victim)", "pass"),
    
    # spells
    "bolt": Spell("bolt", 5, 1, "caster.MP * .75", "caster.AGI", 0, False, "pass", "pass"),
    "flame": Spell("flame", 5, 1, "caster.AGI", "caster.DEX", 0, False, "applyStatus('burn', victim)", "pass"),
    "fireball": Spell("fireball", 15, 1, "caster.MP * 3", "caster.DEX", .25, False, "applyStatus('burn', victim)", "applyStatus('burn', caster)"),
    "nuke": Spell("nuke", 100784, 999, "caster.MaxHP * 99999", inf, 0, True, "pass", "pass"),
    "doom": Spell("doom", 100, 1, "0", "inf", 0, False, "applyStatus('impending doom', victim)", "pass"),

    # buffs
    "warcry": Spell("warcry", 10, 1, "0", "inf", 0, True, "pass", "applyStatus('STR up', caster)"),
    "foresee": Spell("foresee", 10, 1, "0", "inf", 0, True, "pass", "applyStatus('DEX up', cast   er)"),
    "protection": Spell("protection", 10, 1, "0", "inf", 0, True, "pass", "applyStatus('DEF up', caster)"),
    "evasion": Spell("evasion", 10, 1, "0", "inf", 0, True, "pass", "applyStatus('AGI up', caster)"),
    "bunny": Spell("bunny", 50, 1, "0", "inf", 0, True, "applyStatus('bunnied', victim)", "applyStatus('bunny', caster)"),

    # debuffs
    "threaten": Spell("threaten", 10, 1, "0", "inf", 0, True, "applyStatus('STR down', victim)", "pass"),
    "trip": Spell("trip", 10, 1, "0", "inf", 0, True, "applyStatus('DEX down', victim)", "pass"),
    "exploit": Spell("exploit", 10, 1, "0", "inf", 0, True, "applyStatus('DEF down', victim)", "pass"),
    "slow": Spell("slow", 10, 1, "0", "inf", 0, True, "applyStatus('AGI down', victim)", "pass"),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "caster.DEF", "inf", -1, True, "pass", "pass"),
    "courage": Spell("courage", 15, 2, "caster.DEF", "inf", -1.2, True, "pass", "pass"),
    "valor": Spell("valor", 45, 3, "caster.DEF", "inf", -1.8, True, "pass", "if(randint(1,4) == 1): applyStatus('DEF up', caster)"),

    # items

}

statuses = {
    # stat buffs
    "STR up": Status("STR up", 0, True, "victim.STR *= 6/5", "victim.STR /= 6/5"),
    "DEX up": Status("DEX up", 0, True, "victim.DEX *= 6/5", "victim.DEX /= 6/5"),
    "DEF up": Status("DEF up", 0, True, "victim.DEF *= 6/5", "victim.DEF /= 6/5"),
    "AGI up": Status("AGI up", 0, True, "victim.AGI *= 6/5", "victim.AGI /= 6/5"),
    "bunny": Status("bunny", .10, True, "victim.AGI *= 4\nvictim.STR /= 8", "victim.AGI /= 4\nvictim.STR *= 8"),

    "STR up 1": Status("STR up 1", 0, True, "victim.STR += 1", "victim.STR -= 1"),
    "DEX up 1": Status("DEX up 1", 0, True, "victim.DEX += 1", "victim.DEX -= 1"),
    "DEF up 1": Status("DEF up 1", 0, True, "victim.DEF += 1", "victim.DEF -= 1"),
    "AGI up 1": Status("AGI up 1", 0, True, "victim.AGI += 1", "victim.AGI -= 1"),


    # stat debuffs
    "STR down": Status("STR down", 0, True, "victim.STR /= 6/5", "victim.STR *= 6/5"),
    "DEX down": Status("DEX down", 0, True, "victim.DEX /= 6/5", "victim.DEX *= 6/5"),
    "DEF down": Status("DEF down", 0, True, "victim.DEF /= 6/5", "victim.DEF *= 6/5"),
    "AGI down": Status("AGI down", 0, True, "victim.AGI /= 6/5", "victim.AGI *= 6/5"),
    "bunnied": Status("bunnied", .10, True, "victim.DEX /= 4\nvictim.STR /= 4", "victim.DEX *= 4\nvictim.STR *= 4"),

    "STR down 1": Status("STR down 1", 0, True, "victim.STR -= 1", "victim.STR += 1"),
    "DEX down 1": Status("DEX down 1", 0, True, "victim.DEX -= 1", "victim.DEX += 1"),
    "DEF down 1": Status("DEF down 1", 0, True, "victim.DEF -= 1", "victim.DEF += 1"),
    "AGI down 1": Status("AGI down 1", 0, True, "victim.AGI -= 1", "victim.AGI += 1"),

    # DOT effects
    "burn": Status("burn", .25, False, """
burndmg = ceil(victim.MaxHP / 18)
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
    "rat": Entity("rat", 3, inf, 1, 0, 0, 5, ["bite"], {}, []),
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
def calcHit(attackerHit: int, victimDodge: int):
    if (victimDodge < 1): victimDodge = 1
    if (attackerHit < 1): attackerHit = 1
    if (victimDodge == 3): 
        hitChance = round(log(attackerHit * (2.999999 / (victimDodge + 0.0000001))) * 40  ) + 90
    else: 
        hitChance = round(log((attackerHit) * (3 / (victimDodge + 0.0000001))) * 40) + 90
    if (hitChance < 30): hitChance = 30
    if (hitChance >= randint(1,100)): return True
    else: return False

# gives a status effect to an entity
def applyStatus(status: str, victim:object, silent:bool = False):
    status = copy(statuses[status])
    if (silent == False):
        if (victim.name == "you"):
            print("you now have " + status.name)
        else:
            print(victim.name + " now has " + status.name)
    victim.status += [status.name]
    if (status.affectOnApply):
        exec(status.effect)

# removes a status effect from an entity
def removeStatus(status: str, victim:object, silent:bool = False):
    if (status.name in victim.status):
        victim.status.remove(status.name)
        if (silent == False):
            if (victim.name == "you"):
                print("you no longer have " + status.name)
            else:
                print(status.name + " faded from the " + victim.name)

# causes a status effect to execute it's effect
def tickStatus(status: str, victim:object, silent:bool = False):
    status = copy(statuses[status])
    if (status.affectOnApply == False):
        exec(status.effect)
        if (status.fadeChance >= uniform(0,1)):
            removeStatus(status, victim)

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
    if (eval(spell.hitStat) == inf): bypassHit = True
    else: bypassHit = False
    spellHit = False
    for each in range(spell.procs):
        if (bypassHit or calcHit(eval(spell.hitStat), victim.AGI)):
            spellHit = True
            if (spell.ignoreEnemyDEF):
                damage = ceil((eval(spell.dmgStat)) * (randint(100, 115)/100))
            else:
                damage = ceil((eval(spell.dmgStat) * (randint(100, 115)/100)) - victim.DEF)
            if (damage <= 0):
                if (eval(spell.hitStat) != 0):
                    print("0 damage")
            else:
                if (eval(spell.hitStat) != 0):
                    print(str(ceil(damage)) + " damage")
                    victim.HP -= ceil(damage)
                    for each in caster.onHit:
                        exec(each)
                    for each in victim.onHurt:
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

def equip(equipper:object, armor:object, slot:str):
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

def unequip(equipper:object, slot:str):
    armor = equipper.equip[slot]

    equipper.MaxHP -= armor.HP
    if equipper.HP > equipper.MaxHP: equipper.HP = equipper.MaxHP
    equipper.MaxMP -= armor.MP
    if equipper.MP > equipper.MaxMP: equipper.MP = equipper.MaxMP
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

def generateEquip(player:object, dropper: str, baseHealth:int, statups:int = 0, perks:int = 0, quirks:int = 0, slot:str = 'random'):
    if (slot == 'random'):
        slot = choice(['weapon','helmet','chestplate','boots','charm'])
    HP = -statups/(ceil(baseHealth/(10-(2*perks)+(2*quirks))))
    if HP < 0:
        override = HP
        HP = 1
    else:
        override = 0
    HP = round(log(HP) + override)
    MP = 0
    STR = 0
    DEX = 0
    DEF = 0
    AGI = 0
    name = choice(armor_adjectives) + " " + slot + " of the " + dropper.name
    while (name in player.inventory.keys()):
        name = choice(armor_adjectives) + slot + " of the " + dropper.name
    onTurnStart = []
    onAttack = []
    onHit = []
    onCast = []
    onHurt = []
    for each in range(statups):
        increase = choice(["MP", "STR", "DEX", "DEF", "AGI"])
        exec(increase + " += 1")
        if (increase == "MP"):
            MP += 1
    for each in range(perks):
        onWhat = choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
        doWhat = choice(
            "hurt = ceil(enemy.MaxHP / 30)\nenemy.HP -= hurt\nprint('the' + enemy.name + 'took ' + str(heal) + ' damage')",
            "heal = ceil(player.MaxHP / 25)\nplayer.HP += heal\nprint('you healed ' + str(heal) + ' hp')\nif(player.HP > player.MaxHP): player.HP = player.MaxHP",
            "player.HP -= 2\nenemy.HP -= 10\nprint('you took 2 damage')\nprint('the ' + enemy.name + ' took 10 damage)",
            "applyEffect('STR down 1', enemy)",
            "applyEffect('DEX down 1', enemy)",
            "applyEffect('DEF down 1', enemy)",
            "applyEffect('AGI down 1', enemy)",
            "applyEffect('STR up 1', player)",
            "applyEffect('DEX up 1', player)",
            "applyEffect('DEF up 1', player)",
            "applyEffect('AGI up 1', player)",
            "if (randint(1,10) == 1): applyEffect('poison', enemy)",
            "if (randint(1,10) == 1): applyEffect('burn', enemy)"
        )
        exec(onWhat + ".append(" + doWhat +")")
    for each in range(quirks):
        onWhat = choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
        doWhat = choice(
            "hurt = ceil(player.MaxHP / 25)\nplayer.HP -= hurt\nprint('you took ' + str(hurt) + ' damage')\nif(player.HP > player.maxHP): player.HP = player.MaxHP", 
            "heal = ceil(enemy.MaxHP / 25)\nenemy.HP += heal\nprint('the' + enemy.name + 'healed ' + str(heal) + ' hp')\nif(enemy.HP > enemy.maxHP): enemy.HP = enemy.MaxHP"
            "applyEffect('STR up 1', enemy)",
            "applyEffect('DEX up 1', enemy)",
            "applyEffect('DEF up 1', enemy)",
            "applyEffect('AGI up 1', enemy)",
            "applyEffect('STR down 1', player)",
            "applyEffect('DEX down 1', player)",
            "applyEffect('DEF down 1', player)",
            "applyEffect('AGI down 1', player)",
            "if (randint(1,10) == 1): applyEffect('poison', player)",
            "if (randint(1,10) == 1): applyEffect('burn', player)"
        )
        exec(onWhat + ".append(" + doWhat +")")
    return Equipment(name, slot, HP, MP, STR, DEX, DEF, AGI, onTurnStart, onAttack, onCast, onHit, onHurt)
    
# for dictionaries where the key's values are only numbers
def incrementDict(item:str=None, given:dict = {}, change:int=-1):
    if (item == None):
        print("no item given to , returned statement")
        return
    if (item in list(given.keys())):
        given[item] = (given.get(item)) + change
    else:
        given[item] = change
    if (given[item] <= 0):
        given.pop(item)
    return given

# causes a combat to initate between two entities
def doCombat(player: object, enemy: object):
    enemy = copy(monsters[enemy])
    print("a " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        for each in player.onTurnStart:
            exec(each)
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your MP: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = verify("what would you like to do? [attack, spell, item]\n> ", ["attack", "spell", "skill", "item", "a", "s", "i"])
        # player uses attack action
        if (chosen == "attack" or chosen == "a"):
            clearTerminal()
            castSpell("attack", player, enemy)
            # proc on attack abilities
            for each in player.onAttack:
                exec(each)
        # player casts spell
        elif (chosen == "spell" or chosen == "skill" or chosen == "s"):
            # list player's spells
            print("")
            print("your spells:")
            for each in player.spells:
                each = spells[each]
                print(each.name + ": " + str(each.cost) + " MP")
            print("")
            allowed = player.spells + ["back"]
            # let the player choose a spell to cast
            chosen = verify("choose an spell to cast, or type back to go back\n> ", allowed)
            # player wants to go back
            if (chosen == "back"):
                # restart loop (player chooses action again)
                clearTerminal()
                continue
            # player casts a spell
            else:
                clearTerminal()
                # check for enough MP
                if (spells[chosen].cost <= player.MP):
                    # cast the spell
                    castSpell(chosen, player, enemy)
                    # proc on cast abilities
                    for each in player.onCast:
                        exec(each)
                else:
                    # restart loop (player chooses action again)
                    clearTerminal()
                    print("not enough mana!")
                    print("")
                    continue
        # player uses an item
        elif (chosen == "item" or chosen == "i"):
            print("WHAT THE HELL IS AN ITEM *eagle screech*")
            continue
        # proc all of the player's status effects
        for each in player.status:
            tickStatus(each, player)
        # regenerate 1 mana for each 10 max mana the player has
        player.MP += ceil(player.MaxMP / 10)
        # if the player has overflowing mana, bring it back down to the max
        if (player.MP > player.MaxMP): player.MP = player.MaxMP
        # if the player is alive:
        if (enemy.HP > 0):
            # proc enemy's turn start abilities
            for each in enemy.onTurnStart:
                exec(each)
            print("")
            # enemy casts a random spell from their spell list
            castSpell(choice(enemy.spells), enemy, player)
            # proc enemy's on attack abilities
            for each in enemy.onAttack:
                exec(each)
            # proc all of its status effects
            for each in enemy.status:
                tickStatus(each, enemy)
    if (player.HP > 0):
        # remove statuses from player in reverse order
        (player.status).reverse()
        for each in player.status:
            each = copy(statuses[each])
            removeStatus(each, player)
        print("")
        print("victory!")
        # give the player xp points
        xpGain = round(enemy.MaxHP * uniform(1, 1.4)) + randint(0, 3)
        print("you gained " + str(xpGain) + " xp")
        player.XP += xpGain
        del xpGain
        # enemy has a chance to drop equipment
        if (randint(1, 1) == 1):
            dropped = generateEquip(player, enemy, player.level/max((player.level^2)/enemy.MaxHP , 1), round((enemy.STR + enemy.DEX + enemy.DEF + enemy.AGI)/2))
            player.heldarmors[dropped.name] = dropped
            print("the " + enemy.name + " dropped a " + dropped.name)
        # if the player's xp is high enough, increase level
        while (player.XP >= player.MaxXP):
            print("")
            print("<<< level up! >>>")
            print("max HP increased by 5, max MP increased by 2, and all stats increased by 1!")
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
                print("max HP increased by 5")
                print("HP fully restored!")
            elif (chosen == "MP"):
                player.MaxMP += 1
                player.MP = player.MaxMP
                print("max MP increased by 2")
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
        chosen = verify("what will you do? [rest, equip, unequip, drop, leave]\n> ", ["rest", "equip", "unequip", "drop", "leave", "r", "e", "u", "d", "l"])
        if (chosen == "rest" or chosen == "r"):
            if (player.HP >= player.MaxHP and player.MP >= player.MaxMP):
                print("you already feel rested, you don't feel the need to do so again right now")
                input("enter anything to continue...\n> ")
                clearTerminal()
            else:
                player.HP = player.MaxHP
                player.MP = player.MaxMP
                print("MP and HP fully restored!")
                input("enter anything to continue...\n> ")
                clearTerminal()
        elif (chosen == "equip" or chosen == "e"):
            print('\nyour equipment:\n')
            for each in player.heldarmors.keys():
                print(each)
            select = verify("\nwhat would you like to equip? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"])
            if (select == 'back'):
                clearTerminal()
                continue
            elif (select in player.heldarmors.keys()):
                print(player.heldarmors)
                select = player.heldarmors.get(select)
                print(player.equip)
                if (player.equip.get(select.slot, None) is not None):
                    print("you unequip your " + select.name)
                    unequip(player, select.slot)
                print('you equip the ' + select.name)
                equip(player, player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
                input("enter anything to continue...\n> ")
                clearTerminal()
        elif (chosen == "unequip" or chosen == "u"):
            select = verify("\nwhat slot would you like to unequip? type back to go back [weapon, helmet, chestplate, boots, charm] \n> ", ["weapon", "helmet", 'chestplate', 'boots', 'charm', 'back'])
            select = player.equip.get(select)
            if (select != None):
                print("you unequip the " + select.name)
                unequip(player, select.slot)
                player.heldarmors[select.name] = select
            else:
                print("you don't have anything to unequip there! ")
                input("enter anything to continue...\n> ")
        elif (chosen == "drop" or chosen == "d"):
            pass
        elif (chosen == "leave" or chosen == "l"):
            print("")
            input("enter anything to continue...\n> ")
            clearTerminal()
            break

player = Entity("you", 20, 5, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery"], { }, [])

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
