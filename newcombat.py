### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
import random, math, time, copy, os

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

class Modifier:
    def __init__ (self, name:str, code:str):
        self.name = name
        self.code = code

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

class Item:
    def __init__(self, name:str, code:str, usableOutsideCombat:bool):
        self.name = name
        self.code = code
        self.usableOutsideCombat = usableOutsideCombat

class Entity:
    def __init__(self, name: str, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list,
     inventory: dict = {}, blessings: list = [], onTurnStart: list = [], onAttack: list = [], onCast: list = [], 
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
    "nuke": Spell("nuke", 100784*0, 999, "caster.MaxHP * 99999", math.inf, 0, True, "pass", "pass"),
    "doom": Spell("doom", 100, 1, "0", "math.inf", 0, False, "applyStatus('impending doom', victim)", "pass"),

    # buffs
    "warcry": Spell("warcry", 10, 1, "0", "math.inf", 0, True, "pass", "applyStatus('STR up', caster)"),
    "foresee": Spell("foresee", 10, 1, "0", "math.inf", 0, True, "pass", "applyStatus('DEX up', caster)"),
    "protection": Spell("protection", 10, 1, "0", "math.inf", 0, True, "pass", "applyStatus('DEF up', caster)"),
    "evasion": Spell("evasion", 10, 1, "0", "math.inf", 0, True, "pass", "applyStatus('AGI up', caster)"),
    "bunny": Spell("bunny", 50, 1, "0", "math.inf", 0, True, "applyStatus('bunnied', victim)", "applyStatus('bunny', caster)"),

    # debuffs
    "threaten": Spell("threaten", 10, 1, "0", "math.inf", 0, True, "applyStatus('STR down', victim)", "pass"),
    "trip": Spell("trip", 10, 1, "0", "math.inf", 0, True, "applyStatus('DEX down', victim)", "pass"),
    "exploit": Spell("exploit", 10, 1, "0", "math.inf", 0, True, "applyStatus('DEF down', victim)", "pass"),
    "slow": Spell("slow", 10, 1, "0", "math.inf", 0, True, "applyStatus('AGI down', victim)", "pass"),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "caster.DEF", "math.inf", -1, True, "pass", "pass"),
    "courage": Spell("courage", 15, 2, "caster.DEF", "math.inf", -1.2, True, "pass", "pass"),
    "valor": Spell("valor", 45, 3, "caster.DEF", "math.inf", -1.8, True, "pass", "if(random.randint(1,4) == 1): applyStatus('DEF up', caster)"),

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
burndmg = math.ceil(victim.MaxHP / 18)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from burn')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from burn')
victim.HP -= burndmg
del burndmg""", "pass"),

    "poison": Status("poison", .1, False, """
burndmg = math.ceil(victim.MaxHP / 20)
if (victim.name == "you"):
    print('you took ' + str(burndmg) + ' damage from poison')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from poison')
victim.HP -= burndmg
del burndmg""", "pass"),

    # other
    "impending doom": Status("impending doom", .5, False, "pass", "applyStatus('doom', victim)"),
    "doom": Status("doom", 0, False, "print('death calls.')\nprint('your HP drops to 0')\nvictim.HP = 0", "pass"),
}

monsters = {
    # forest
    "rat": Entity("rat", 3, math.inf, 1, 0, 0, 5, ["bite"]),
    "wolf": Entity("wolf", 15, math.inf, 2, 3, 1, 1, ["attack"]),
    "spirit": Entity("spirit", 25, math.inf, 4, 5, 0, 4, ["attack", "flame"]),

    # infernal wastes
    "imp": Entity('imp', 70, math.inf, 10, 15, -5, 20, ["evasion", "attack", "flame", "threaten"]),
    "demon": Entity('demon', 100, math.inf, 25, 10, 6, 10, ["attack", "flame", "courage", "warcry", "foresee"]),
    "warg": Entity('warg', 150, math.inf, 10, 20, 10, 10, ["bite", "tricut"], {}, [], ["applyStatus('STR up', enemy)"]),

    # what the hell
    "reaper": Entity("reaper", 666, math.inf, 100, 200, 50, 100, ["doom", "bunny", "evasion", "trip"]),
    "minor deity": Entity("minor deity", 7777, math.inf, 100, 1000, 50, 50, ["evasion"])
}

# calculates if an attack should hit a given entity
def calcHit(attackerHit: int, victimDodge: int):
    if (victimDodge < 1): victimDodge = 1
    if (attackerHit < 1): attackerHit = 1
    if (math.isinf(attackerHit)): bypassHit = True
    else: bypassHit = False
    if (bypassHit):
        return True
    else:
        if (victimDodge == 3): 
            hitChance = round(math.log(attackerHit * (2.999999 / (victimDodge + 0.0000001))) * 40  ) + 90
        else: 
            hitChance = round(math.log((attackerHit) * (3 / (victimDodge + 0.0000001))) * 40) + 90
    if (hitChance < 30): hitChance = 30
    if (hitChance >= random.randint(1,100)): return True
    else: return False

# gives a status effect to an entity
def applyStatus(status: str, victim:object, silent:bool = False):
    status = copy.copy(statuses[status])
    if (silent == False):
        if (victim.name == "you"):
            print("you now have " + status.name)
        else:
            print(victim.name + " now has " + status.name)
    victim.status += [status]
    if (status.affectOnApply):
        exec(status.effect)

# removes a status effect from an entity
def removeStatus(status: str, victim:object, silent:bool = False):
#     if (status.name in victim.status):
#         victim.status.remove(status.name)
#         exec(status.reverseEffect)
#         if (silent == False):
#             if (victim.name == "you"):
#                 print("you no longer have " + status.name)
#             else:
#                 print(status.name + " faded from the " + victim.name)
#     else:
#         raise(f"A status effect was attempted to be removed on {victim.name}, but it didn't exist in {victim.name}'s status list.")
    status = copy.copy(statuses[status])
    if (status.name in victim.status):
        statusIndex = victim.status.index(status)
        if (len(victim.status) > 1): firstHalf = victim.status[:statusIndex]
        else: firstHalf = []
        secondHalf = victim.status[statusIndex:]
        removed = secondHalf.pop(0)
        exec(removed.reverseStatus)
        if (silent == False):
            if (victim.name == "you"):
                print("you no longer have " + status.name)
            else:
                print(status.name + " faded from the " + victim.name)
        for each in secondHalf:
            applyStatus(status, victim, True)
            firstHalf.append(each)
    else:
        raise IndexError(f"A status effect was attempted to be removed on {victim.name}, but it didn't exist in {victim.name}'s status list.")

# causes a status effect to execute it's effect
def tickStatus(status: str, victim:object, silent:bool = False):
    status = copy.copy(statuses[status.name])
    if (status.affectOnApply == False):
        exec(status.effect)
        if (status.fadeChance >= random.uniform(0,1)):
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
    if (spell.hitStat == math.inf): bypassHit = True
    else: bypassHit = False
    spellHit = False
    for each in range(spell.procs):
        if (bypassHit or calcHit(eval(spell.hitStat), victim.AGI)):
            spellHit = True
            if (spell.ignoreEnemyDEF):
                damage = math.ceil((eval(spell.dmgStat)) * (random.randint(100, 115)/100))
            else:
                damage = math.ceil((eval(spell.dmgStat) * (random.randint(100, 115)/100)) - victim.DEF)
            if (damage <= 0):
                if (spell.hitStat != 0):
                    print("0 damage")
            else:
                if (spell.hitStat != 0):
                    print(str(math.ceil(damage)) + " damage")
                    victim.HP -= math.ceil(damage)
                    for each in caster.onHit:
                        exec(each)
                    for each in victim.onHurt:
                        exec(each)
        else:
            print("miss")
            damage = 0
        casterDamage = damage * spell.damageRecoil
        if (casterDamage != 0):
            casterDamage = math.ceil(casterDamage)
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
    subtract = lambda x, y: x - y
    def diff(input1, input2):
        return str(subtract(input1, input2))

    savedMaxHP = equipper.MaxHP
    savedMaxMP = equipper.MaxMP
    savedSTR = equipper.STR
    savedDEX = equipper.DEX
    savedDEF = equipper.DEF
    savedAGI = equipper.AGI

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

    print("\nHP: " + diff(equipper.MaxHP, savedMaxHP))
    print("MP: " + diff(equipper.MaxMP, savedMaxMP))
    print("STR: " + diff(equipper.STR,savedSTR))
    print("DEX: " + diff(equipper.DEX,savedDEX))
    print("DEF: " + diff(equipper.DEF,savedDEF))
    print("AGI: " + diff(equipper.AGI,savedAGI))

    if equipper.HP > equipper.MaxHP: equipper.HP = equipper.MaxHP
    if equipper.MaxHP < 0: print("warning: your max hp is less than 0! increase your max hp and heal, or you'll die after your next turn")
    if equipper.HP < 0: print("warning: your hp is less than 0! heal before you go into your next fight, or you'll die after your next turn")

def unequip(equipper:object, slot:str):
    subtract = lambda x, y: x - y
    def diff(input1, input2):
        return str(subtract(input1, input2))

    savedMaxHP = equipper.MaxHP
    savedMaxMP = equipper.MaxMP
    savedSTR = equipper.STR
    savedDEX = equipper.DEX
    savedDEF = equipper.DEF
    savedAGI = equipper.AGI

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

    print("\nHP: " + diff(equipper.MaxHP, savedMaxHP))
    print("MP: " + diff(equipper.MaxMP, savedMaxMP))
    print("STR: " + diff(equipper.STR,savedSTR))
    print("DEX: " + diff(equipper.DEX,savedDEX))
    print("DEF: " + diff(equipper.DEF,savedDEF))
    print("AGI: " + diff(equipper.AGI,savedAGI))

    if equipper.HP > equipper.MaxHP: equipper.HP = equipper.MaxHP
    if equipper.MaxHP < 0: print("warning: your max hp is less than 0! you will die after your next turn if you don't increase your max hp and rest")
    if equipper.HP < 0: print("warning: your hp is less than 0! heal before you go into your next fight, or you'll die after your next turn")

def generateEquip(player:object, dropper: str, baseHealth:int, statups:int = 0, perks:int = 0, quirks:int = 0, slot:str = 'random'):
    if (slot == 'random'):
        slot = random.choice(['weapon','helmet','chestplate','boots','charm'])
    name = random.choice(armor_adjectives) + " " + slot + " of the " + dropper.name
    while (name in player.inventory.keys()):
        name = random.choice(armor_adjectives) + slot + " of the " + dropper.name
    # bonusHP = statups/max(math.ceil(baseHealth/(10-(2*perks)+(2*quirks))), 1)
    # if bonusHP < 0:
    #     override = bonusHP
    #     bonusHP = 1
    # else:
    #     override = 0
    # bonusHP = round(log(bonusHP) + override)
    bonusHP = baseHealth

    list_of_things = [0, 0, 0, 0, 0]
    for _ in range(statups):
        index = -1
        a = random.randint(0,4)
        for _ in list_of_things:
            index += 1
            if a == index: 
                list_of_things[index] += random.randint(1,2) 
    bonusMP = list_of_things[0]
    bonusSTR = list_of_things[1]
    bonusDEX = list_of_things[2]
    bonusDEF = list_of_things[3]
    bonusAGI = list_of_things[4]

    onTurnStart = []
    onAttack = []
    onHit = []
    onCast = []
    onHurt = []
    for _ in list(range(perks)):
        onWhat = random.choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
        doWhat = random.choice(
            "hurt = math.ceil(enemy.MaxHP / 30)\nenemy.HP -= hurt\nprint('the' + enemy.name + 'took ' + str(heal) + ' damage')",
            "heal = math.ceil(player.MaxHP / 25)\nplayer.HP += heal\nprint('you healed ' + str(heal) + ' hp')\nif(player.HP > player.MaxHP): player.HP = player.MaxHP",
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
    for _ in list(range(quirks)):
        onWhat = random.choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
        doWhat = random.choice(
            "hurt = math.ceil(player.MaxHP / 25)\nplayer.HP -= hurt\nprint('you took ' + str(hurt) + ' damage')\nif(player.HP > player.maxHP): player.HP = player.MaxHP", 
            "heal = math.ceil(enemy.MaxHP / 25)\nenemy.HP += heal\nprint('the' + enemy.name + 'healed ' + str(heal) + ' hp')\nif(enemy.HP > enemy.maxHP): enemy.HP = enemy.MaxHP"
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
    return Equipment(name, slot, round(bonusHP), round(bonusMP), round(bonusSTR), round(bonusDEX), round(bonusDEF), round(bonusAGI), onTurnStart, onAttack, onCast, onHit, onHurt)
    
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
    enemy = copy.copy(monsters[enemy])
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
            index = 0
            for each in player.spells:
                each = spells[each]
                print(f"{index}. {each.name}: {each.cost} MP")
                index += 1
            weirdlist = list(range(len(player.spells)))
            weirdlist = [str(each) for each in weirdlist]
            allowed = player.spells + ["back"] + weirdlist
            # let the player choose a spell to cast
            chosen = verify("\nchoose an spell to cast, or type back to go back\n> ", allowed)
            # player wants to go back
            if (chosen == "back"):
                # restart loop (player chooses action again)
                clearTerminal()
                continue
            # player casts a spell
            else:
                if (chosen not in player.spells):
                    chosen = player.spells[int(chosen)]
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
        player.MP += math.ceil(player.MaxMP / 10)
        # if the player has overflowing mana, bring it back down to the max
        if (player.MP > player.MaxMP): player.MP = player.MaxMP
        # if the player is alive:
        if (enemy.HP > 0):
            # proc enemy's turn start abilities
            for each in enemy.onTurnStart:
                exec(each)
            print("")
            # enemy casts a random spell from their spell list
            castSpell(random.choice(enemy.spells), enemy, player)
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
            each = copy.copy(statuses[each])
            removeStatus(each, player, True)
        print("")
        print("victory!")
        # give the player xp points
        xpGain = round(enemy.MaxHP / 2 * random.uniform(1, 1.4))
        print("you gained " + str(xpGain) + " xp")
        player.XP += xpGain
        del xpGain
        # enemy has a chance to drop equipment
        dropchance = round(max(random.normalvariate(.4, 1), 0))
        if (dropchance > 0):
            print("\nhere's what you found:\n")
            for _ in range(dropchance):
                dropped = generateEquip(player, enemy, round(math.log(enemy.MaxHP)*(player.level^2)), math.floor((enemy.STR + enemy.DEX + enemy.DEF + enemy.AGI)/3))
                player.heldarmors[dropped.name] = dropped 
                print(" + " + dropped.name)
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
                print(f"max HP increased by {str(3)}")
                print("HP fully restored!")
            elif (chosen == "MP"):
                player.MaxMP += 2
                player.MP = player.MaxMP
                print(f"max MP increased by {str(2)}")
                print("MP fully restored!")
            else:
                exec(f"player.{chosen} += {1}")
                print(f"{chosen} increased by {str(1)}")
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
    randchoice = random.choice(["campfire", "campsite", "clearing", "small ruin"])
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
            index = 0
            for each in player.heldarmors.keys():
                print(f"{index}. {each}")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = verify("\nwhat would you like to equip? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
            if (select == 'back'):
                clearTerminal()
                continue
            elif (select in player.heldarmors.keys()):
                select = player.heldarmors.get(select)
                if (player.equip.get(select.slot, None) != None):
                    toUnequip = player.equip.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    unequip(player, toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                equip(player, player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
                input("enter anything to continue...\n> ")
                clearTerminal()
            else:
                select = int(select)
                select = list(player.heldarmors.keys())[select]
                select = player.heldarmors.get(select)
                if (player.equip.get(select.slot, None) != None):
                    toUnequip = player.equip.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    unequip(player, toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                equip(player, player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
                input("enter anything to continue...\n> ")
                clearTerminal()
        elif (chosen == "unequip" or chosen == "u"):
            select = verify("\nwhat slot would you like to unequip? type back to go back [weapon, helmet, chestplate, boots, charm] \n> ", ["weapon", "helmet", 'chestplate', 'boots', 'charm', 'back'])
            if (select == "back"):
                clearTerminal()
                continue            
            select = player.equip.get(select)
            if (select != None):
                print("you unequip the " + select.name)
                unequip(player, select.slot)
                player.heldarmors[select.name] = select
            else:
                print("you don't have anything to unequip there! ")
            input("enter anything to continue...\n> ")
            clearTerminal()
        elif (chosen == "drop" or chosen == "d"):
            clearTerminal()
            print('\nyour equipment:\n')
            index = 0
            for each in player.heldarmors.keys():
                print(f"{index}. {each}")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = verify("\nwhat would you like to drop? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
            if (select == 'back'):
                clearTerminal()
                continue
            elif (select in player.heldarmors.keys()):
                player.heldarmors.pop(select)
                print("\nyou dropped your " + select)
            else:
                select = int(select)
                select = list(player.heldarmors.keys())[select]
                player.heldarmors.pop(select)
                print("\nyou dropped your " + select)
            input("\nenter anything to continue...\n> ")
            clearTerminal()
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
print("your experience with fighting spirits and fiends have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
player.spells += ["flame", "fireball"]
print("")
input("enter anything to continue...\n> ")
clearTerminal()
doCombat(player, "warg")
restSite(player)
doCombat(player, "reaper")
print("wowie.")
