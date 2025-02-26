### man, my old code is very SPAGHETTI and INEFFICIENT ###
### let's streamline this hunk of junk ###
import random, math, copy, os

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

# clear funky terminal code
os.system('cls' if os.name == 'nt' else 'clear')

class Spell:
    def __init__(self, name: str, cost: int, procs: int, dmgStat: str, hitStat: str, damageRecoil: float = 0, ignoreEnemyDEF: bool = False, victimEffect: str = "pass", selfEffect: str = "pass", description: str = "This is a spell."):
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
        # spell description, duh
        self.description = description

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
    def __init__(self, name:str, code:str, minLevel:int, usableOutsideCombat:bool = False):
        self.name = name
        self.code = code
        self.minLevel = minLevel
        self.usableOutsideCombat = usableOutsideCombat

class Entity:
    def __init__(self, name: str, HP: int, MP: int, STR: int, DEX: int, DEF: int, AGI: int, spells: list,
     inventory: dict = {}, gold: int = 0, blessings: list = [], onTurnStart: list = [], onAttack: list = [], onCast: list = [], 
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
        # MONEYYYYY
        self.gold = gold
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
    "attack": Spell("attack", 0, 1, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "A basic attack, known by most."),
    "doublecut": Spell("doublecut", 5, 2, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "The caster attacks twice in quick succession."),
    "tricut": Spell("tricut", 8, 3, "caster.STR", "caster.DEX", 0, False, "pass", "pass", "The caster attacks thrice in quick succession."),
    "bite": Spell("bite", 2, 1, "caster.STR * .5", "caster.STR", 0, False, "applyStatus('poison', victim)", "pass", "The user bites down on their opponent, inflicting poison."),
    
    # spells
    "bolt": Spell("bolt", 5, 1, "caster.MP", "caster.AGI", 0, False, "pass", "pass", "Cast a small bolt of mana at the user's foe, dealing damage equal to their current MP, before MP deduction."),
    "bolt volley": Spell("bolt volley", 15, 5, "caster.MP", "caster.AGI / 1.5", 0, False, "pass", "pass", "The user casts 'bolt' five times in quick succession with reduced accuracy."),
    "flame": Spell("flame", 5, 1, "caster.DEF", "caster.DEX", 0, False, "applyStatus('burn', victim)", "pass", "Fire a small flame at the user's foe, dealing damage and burning them."),
    "fireball": Spell("fireball", 15, 1, "caster.DEF * 3", "caster.DEX", .25, False, "applyStatus('burn', victim)", "pass", "Summon a large fireball, dealing damage equal to 3 times the caster's DEF and burning the user's foe, but hurts the caster in the process."),
    "nuke": Spell("nuke", 100784, 999, "caster.MaxHP * 99999", math.inf, 0, True, "pass", "pass", "An ancient magic, long lost to time. Requires a unfeasible amount of mana to cast, but is sure to obliterate any foe that opposes its user."),
    "doom": Spell("doom", 100, 1, "0", "math.inf", 0, False, "applyStatus('impending doom', victim)", "pass", "..."),

    # buffs
    "warcry": Spell("warcry", 6, 1, "0", "math.inf", 0, True, "pass", "applyStatus('STR up', caster)", "The caster makes a loud battle cry, increasing the their STR by 20%."),
    "foresee": Spell("foresee", 6, 1, "0", "math.inf", 0, True, "pass", "applyStatus('DEX up', caster)", "Focuses the caster's mind on their opponent's movements, increasing the user's DEX by 20%."),
    "protection": Spell("protection", 6, 1, "0", "math.inf", 0, True, "pass", "applyStatus('DEF up', caster)", "The caster puts their guard up, increasing their DEF by 20%."),
    "evasion": Spell("evasion", 6, 1, "0", "math.inf", 0, True, "pass", "applyStatus('AGI up', caster)", "Become ready to dodge at a moment's notice, increasing the caster's AGI by 20%."),
    "bunny": Spell("bunny", 9, 1, "0", "math.inf", 0, True, "pass", "applyStatus('bunny', caster)", f"Magically transforms the user into a bunny, cutting their STR by 87.5% in exchange for 4 times the AGI."),

    # debuffs
    "threaten": Spell("threaten", 6, 1, "0", "math.inf", 0, True, "applyStatus('STR down', victim)", "pass", "The caster threatens their opponent, decreasing the victim's STR by 20%."),
    "slow": Spell("slow", 6, 1, "0", "math.inf", 0, True, "applyStatus('DEX down', victim)", "pass", "Slows down the caster's foe, decreasing their DEX by 20%."),
    "exploit": Spell("exploit", 6, 1, "0", "math.inf", 0, True, "applyStatus('DEF down', victim)", "pass", "Finds a weakness in the caster's foe, decreasing their DEF by 20%."),
    "trip": Spell("trip", 6, 1, "0", "math.inf", 0, True, "applyStatus('AGI down', victim)", "pass", "Trips up the user's foe, lowering their AGI by 20%."),

    # healing & other
    "bravery": Spell("bravery", 5, 1, "caster.DEF", "math.inf", -1, True, "pass", "pass", "Grants the caster a surge of determination, restoring health equal to the caster's DEF."),
    "courage": Spell("courage", 15, 2, "caster.DEF", "math.inf", -1.5, True, "pass", "pass", "Channels the caster's resolve into healing their wounds, restoring HP equal to 1.5 times the caster's DEF."),
    "valor": Spell("valor", 45, 3, "caster.DEF", "math.inf", -2, True, "pass", "if(random.randint(1,2) == 1): applyStatus('DEF up', caster)", "The caster steels themself with unwavering valor, healing HP equal to 2 times the caster's DEF"),
    "cleanse": Spell("cleanse", 8, 1, "0", "math.inf", 0, True, "pass", "print('you have been cleansed of all statuses')\nfor each in caster.status: removeStatus(each, victim, True)", "Cleanses the user of all status effects, including buffs.")
}

items = {
    # healing
    "small heal": Item("small heal", "print('you sip the small healing potion')\nplayer.HP += 10\nprint('you heal 10 HP')", 1, True),
    "medium heal": Item("medium heal", "print('you drink the medium healing potion')\nplayer.HP += 50\nprint('you heal 50 HP')", 4, True),
    "large heal": Item("large heal", "print('you chug the large healing potion')\nplayer.HP += 100\nprint('you heal 100 HP')", 10, True),
    "massive heal": Item("massive heal", "print('you reluctantly gulp down the massive healing potion...')\nplayer.HP += 200\nprint('you heal 200 HP')", 20, True),
    "panacea": Item("panacea", """
print('you savor the panacea')
for each in player.status:
    removeStatus(each, player, True)
print('you are cured of all statuses')""", 2, True),

    # mana regen
    "small mana": Item("small mana", "print('you sip the small mana potion')\nplayer.MP += 5\nprint('you gain 5 MP')", 1, True),
    "medium mana": Item("medium mana", "print('you drink the medium mana potion')\nplayer.MP += 20\nprint('you gain 20 MP')", 5, True),
    "large mana": Item("large mana", "print('you chug the large mana potion')\nplayer.MP += 50\nprint('you gain 50 MP')", 10, True),
    "massive mana": Item("massive mana", "print('you reluctantly gulp down the massive mana potion...')\nplayer.MP += 100\nprint('you gain 100 MP')", 20, True),
    
    # tonics
    "pepper tonic": Item("pepper tonic", "print('you drink the pepper tonic... spicy!')\napplyStatus('STR up', player, False)", 1),
    "carrot tonic": Item("carrot tonic", "print('you drink the carrot tonic... tastes like carrots.')\napplyStatus('DEX up', player, False)", 1),
    "ginger tonic": Item("ginger tonic", "print('you drink the ginger tonic... so bitter!')\napplyStatus('DEF up', player, False)", 1),
    "wind tonic": Item("wind tonic", """print("you drink the wind tonic... it's empty..?")\napplyStatus('AGI up', player, False)""", 1),

    # weapons
    "throwing knife": Item("throwing knife", "ouch = max(round((player.STR+player.DEX)/2), 1)\nenemy.HP -= ouch\nprint(f'you huck the throwing knife at the {enemy.name} for {ouch} damage')",2)
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

    "STR down 1": Status("STR down 1", 0, True, "victim.STR -= 1", "victim.STR += 1"),
    "DEX down 1": Status("DEX down 1", 0, True, "victim.DEX -= 1", "victim.DEX += 1"),
    "DEF down 1": Status("DEF down 1", 0, True, "victim.DEF -= 1", "victim.DEF += 1"),
    "AGI down 1": Status("AGI down 1", 0, True, "victim.AGI -= 1", "victim.AGI += 1"),

    # DOT effects
    "burn": Status("burn", .25, False, """
burndmg = math.ceil(victim.MaxHP / 18)
if victim.name == "you":
    print('you took ' + str(burndmg) + ' damage from burn')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from burn')
victim.HP -= burndmg
del burndmg""", "pass"),

    "poison": Status("poison", .1, False, """
burndmg = math.ceil(victim.MaxHP / 20)
if victim.name == "you":
    print('you took ' + str(burndmg) + ' damage from poison')
else:
    print('the ' + victim.name + ' took ' + str(burndmg) + ' damage from poison')
victim.HP -= burndmg
del burndmg""", "pass"),

    # other
    "impending doom": Status("impending doom", .05, False, "pass", "applyStatus('doom', victim)\nremoveStatus(statuses['impending doom'], victim, True)"),
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
    "minor deity": Entity("minor deity", 7777, math.inf, 100, 1000, 50, 50, ["evasion"]),

    # other
    "test dummy": Entity('test dummy', 99999, math.inf, 0, 99999, 0, 0, ['bite'])
}

perks = {

}

quirks = {

}

# calculates if an attack should hit a given entity
def calcHit(attackerHit: int, victimDodge: int):
    if victimDodge < 1: victimDodge = 1
    if attackerHit < 1: attackerHit = 1
    if math.isinf(attackerHit): bypassHit = True
    else: bypassHit = False
    if bypassHit:
        return True
    else:
        if victimDodge == 3: 
            hitChance = round(math.log(attackerHit * (2.999999 / (victimDodge + 0.0000001))) * 40  ) + 90
        else: 
            hitChance = round(math.log((attackerHit) * (3 / (victimDodge + 0.0000001))) * 40) + 90
    if hitChance < 30: hitChance = 30
    if hitChance >= random.randint(1,100): return True
    else: return False

# gives a status effect to an entity
def applyStatus(status: str, victim:object, silent:bool = False):
    status = statuses[status]
    if silent == False:
        if victim.name == "you":
            print("you now have " + status.name)
        else:
            print(victim.name + " now has " + status.name)
    victim.status += [status]
    if status.affectOnApply:
        exec(status.effect)

# removes a status effect from an entity
def removeStatus(status: object, victim:object, silent:bool = False):
    if status in victim.status: 
        statusIndex = victim.status.index(status)
        if len(victim.status) > 1: firstHalf = victim.status[:statusIndex]
        else: firstHalf = []
        secondHalf = victim.status[statusIndex:]
        secondHalf.reverse()
        for each in secondHalf: exec(each.reverseEffect)
        secondHalf.reverse()    
        removed = secondHalf.pop(0)
        exec(removed.reverseEffect)
        if silent == False:
            if victim.name == "you":
                print("you no longer have " + status.name)
            else:
                print(status.name + " faded from the " + victim.name)
        for each in secondHalf:
            applyStatus(each.name, victim, True)
            firstHalf.append(each)
        victim.status = firstHalf

# causes a status effect to execute it's effect
def tickStatus(status:object, victim:object, doFadeChance:bool = True):
    if status.affectOnApply == False:
        exec(status.effect)
        if doFadeChance and status.fadeChance >= random.uniform(0,1):
            removeStatus(status, victim)

def castSpell(spell:object, caster:object, victim:object):
    spell = spells[spell]
    if caster.name != "you":
        if spell.name == "attack":
            print("the " + caster.name + " attacks")
        else:
            print("the " + caster.name + " casts " + spell.name + "!")
    else:
        if spell.name == "attack":
            print(caster.name + " attack")
        else:
            print(caster.name + " cast " + spell.name + "!")
    if spell.hitStat == math.inf: bypassHit = True
    else: bypassHit = False
    spellHit = False
    for each in range(spell.procs):
        if bypassHit or calcHit(eval(spell.hitStat), victim.AGI):
            spellHit = True
            if spell.ignoreEnemyDEF:
                damage = math.ceil((eval(spell.dmgStat)) * (random.randint(100, 115)/100))
            else:
                damage = math.ceil((eval(spell.dmgStat) * (random.randint(100, 115)/100)) - victim.DEF)
            if damage <= 0 and spell.hitStat != math.inf:
                print("0 damage")
            elif spell.hitStat != 0:
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
        if casterDamage != 0:
            casterDamage = math.ceil(casterDamage)
            if caster.name == "you":
                if casterDamage < 0:
                    print("you healed " + str(casterDamage * -1) + " hp")
                else:
                    print("you took " + str(casterDamage) + " damage from recoil")
            else:
                if casterDamage < 0:
                    print("the " + caster.name + " healed " + str(casterDamage * -1) + " hp")
                else:
                    print("the " + caster.name + " took " + str(casterDamage) + " damage from recoil")
            caster.HP -= casterDamage
            if caster.HP > caster.MaxHP: caster.HP = caster.MaxHP
    if spellHit:
        exec(spell.victimEffect)
    exec(spell.selfEffect)
    print("")
    caster.MP -= spell.cost
    if victim.HP < 0: victim.HP = 0
    if caster.name != "you": print("your hp: " + str(victim.HP) + " / " + str(victim.MaxHP))
    else: print(victim.name + " hp: " + str(victim.HP) + " / " + str(victim.MaxHP))

# provided a list and a question, forces the player to make a choice from the list
def verify(question:str, allowed:list):
    index = 0
    for each in allowed:
        if isinstance(each, str): allowed[index] = each.lower()
        index += 1
    del index
    while True:
        chosen = input(question)
        if isinstance(chosen, str) == False: chosen = str(chosen) 
        chosen = chosen.lower()
        if chosen.startswith("/"):
            if chosen == "/help":
                print("/help - displays this menu")
                print("/stats - displays your current stats")
                print("/inventory || /inv - shows your inventory and gold")
                print("/spell <spellName> - gives you information regarding the spell provided")
                print("/credits - the beautiful people who worked on this game")
                print("/quit - quits the game")
                print("/patchnotes - shows the patch notes :)")
            elif chosen == "/stats":
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
            elif chosen == "/patchnotes":
                raise ValueError('Variable "patchnotes" is too long to print. Try separating the variable into two different print statements.')
            elif chosen == "/quit":
                print("bye!")
                quit()
            elif chosen == "/inventory" or chosen == "/inv":
                print(f"your gold: {player.gold}")
                print("\nyour items:")
                for eachKey, eachValue in player.inventory.items():
                    print(f"{eachKey.name}: {eachValue}")
                print("")
                print("your equips:")
                for key, value in player.heldarmors.items():
                    print(f"{key}: [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
            elif chosen == "/credits":
                print("")
                print("troy semos - main developer")
                print("jaxon tran - one of the only people who can understand my code and resident crazy idea man")
                print("odin simonson -  can understand my code and professional patch notes enjoyer")
                print("")
            elif "/spell " in chosen:
                spellName = chosen.removeprefix("/spell ")
                if spellName in spells.keys():
                    print(f"\n- {spells[spellName].description}\n")
                else:
                    print("invalid spell name.\n")
            else:
                print("invalid command. to see all valid commands, do /help")
        for i in allowed:
            if isinstance(i, str): i = i.lower()
            if chosen == i:
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

    equipper.HP += armor.HP
    equipper.MaxHP += armor.HP
    equipper.HP += armor.MP
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

def generateEquip(player:Entity, dropperName: str, baseHealth:int, statups:int = 0, perks:int = 0, quirks:int = 0, slot:str = 'random'):
    if slot == 'random':
        slot = random.choice(['weapon','helmet','chestplate','boots','charm'])
    name = random.choice(armor_adjectives) + " " + slot + " of the " + dropperName
    while (name in player.inventory.keys() or name in player.equip.values()):
        name = random.choice(armor_adjectives) + slot + " of the " + dropperName
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
            "applyEffect('STR down', enemy)",
            "applyEffect('DEX down', enemy)",
            "applyEffect('DEF down', enemy)",
            "applyEffect('AGI down', enemy)",
            "applyEffect('STR up', player)",
            "applyEffect('DEX up', player)",
            "applyEffect('DEF up', player)",
            "applyEffect('AGI up', player)",
            "if(randint(1,10) == 1: applyEffect('poison', enemy)",
            "if randint(1,10) == 1: applyEffect('burn', enemy)"
        )
        exec(onWhat + ".append(" + doWhat +")")
    for _ in list(range(quirks)):
        onWhat = random.choice("onTurnStart", "onAttack", "onCast", "onHit", "onHurt")
        doWhat = random.choice(
            "hurt = math.ceil(player.MaxHP / 25)\nplayer.HP -= hurt\nprint('you took ' + str(hurt) + ' damage')\nif(player.HP > player.maxHP): player.HP = player.MaxHP", 
            "heal = math.ceil(enemy.MaxHP / 25)\nenemy.HP += heal\nprint('the' + enemy.name + 'healed ' + str(heal) + ' hp')\nif(enemy.HP > enemy.maxHP): enemy.HP = enemy.MaxHP"
            "applyEffect('STR up', enemy)",
            "applyEffect('DEX up', enemy)",
            "applyEffect('DEF up', enemy)",
            "applyEffect('AGI up', enemy)",
            "applyEffect('STR down', player)",
            "applyEffect('DEX down', player)",
            "applyEffect('DEF down', player)",
            "applyEffect('AGI down', player)",
            "if randint(1,10) == 1: applyEffect('poison', player)",
            "if randint(1,10) == 1: applyEffect('burn', player)"
        )
        exec(onWhat + ".append(" + doWhat +")")
    return Equipment(name, slot, round(bonusHP), round(bonusMP), round(bonusSTR), round(bonusDEX), round(bonusDEF), round(bonusAGI), onTurnStart, onAttack, onCast, onHit, onHurt)
    
# for dictionaries where the key's values are only numbers *wink wink inventory*
def incrementDict(item:Item, given:dict, change:int=1):
    if item in list(given.keys()):
        given[item] = (given.get(item)) + change
    else:
        given[item] = change
    if given[item] <= 0:
        given.pop(item)
    return given

# causes a combat to initate between two entities
def doCombat(player: Entity, enemy: Entity):
    enemy = copy.copy(monsters[enemy])
    print("a " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        for each in player.onTurnStart:
            exec(each)
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your MP: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = verify("what would you like to do? [attack, spell, item, pass]\n> ", ["attack", "spell", "skill", "item", "pass", "a", "s", "i", "p"])
        print("")
        # player uses attack action (secretly just a free spell)
        if chosen == "attack" or chosen == "a":
            castSpell("attack", player, enemy)
            # proc on attack abilities
            for each in player.onAttack:
                exec(each)
        # player casts spell
        elif chosen == "spell" or chosen == "skill" or chosen == "s":
            # list player's spells
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
            chosen = verify("\nchoose a spell to cast, or type back to go back\n> ", allowed)
            # player wants to go back
            if chosen == "back":
                # restart loop (player chooses action again)
                continue
            # player casts a spell
            else:
                if chosen not in player.spells:
                    chosen = player.spells[int(chosen)]
                # check for enough MP
                if spells[chosen].cost <= player.MP:
                    # cast the spell
                    castSpell(chosen, player, enemy)
                    # proc on cast abilities
                    for each in player.onCast:
                        exec(each)
                else:
                    # player acts again 
                    print("not enough mana!")
                    print("")
                    continue
        # player uses an item
        elif chosen == "item" or chosen == "i":
            print("your items:")
            allowed = []
            index = 0
            for key in player.inventory:
                value = player.inventory[key]
                print(f"{index}. {key.name}: {value}")
                allowed.append(key.name)
                index += 1
            allowed += list(range(len(allowed)))
            index = 0
            for each in allowed:
                allowed[index] = str(each)
                index += 1
            allowed += ["back"]
            chosen = verify("\nchoose an item to use, or type back to go back\n> ", allowed)
            if chosen == "back": continue
            else:
                if chosen.isdigit(): chosen = allowed[int(chosen)]
                usedItem = items[chosen]
                exec(usedItem.code)
                incrementDict(usedItem, player.inventory, -1)
                if player.HP > player.MaxHP: player.HP = player.MaxHP
                if player.MP > player.MaxMP: player.MP = player.MaxMP
        elif chosen == "pass" or chosen == "p":
            print("you wait")    
        # proc all of the player's status effects
        for each in player.status:
            tickStatus(each, player, (enemy.HP > 0))
        # regenerate 1 mana for each 10 max mana the player has
        if not math.isinf(player.MP): player.MP += math.ceil(player.MaxMP / 10)
        if player.MP > player.MaxMP: player.MP = player.MaxMP
        # if the enemy is alive:    
        if enemy.HP > 0:
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
    if player.HP > 0:
        # remove statuses from player in reverse order
        (player.status).reverse()
        for each in player.status:
            removeStatus(each, player, True)
        print("")
        print("victory!")
        # give the player xp points
        xpGain = round(enemy.MaxHP / 2 * random.uniform(1, 1.4))
        print("you gained " + str(xpGain) + " xp")
        player.XP += xpGain
        del xpGain
        # enemy has a chance to drop equipment
        # do the same with consumables
        dropchance = math.floor(max(random.normalvariate(.4, 1), 0))
        itemDropchance = math.floor(max(random.normalvariate(1, 1), 0))
        numEquipped = 0
        for each in player.equip.values():
            if each != None:
                numEquipped += 1
        if dropchance < 1 and numEquipped <= 1: dropchance = 1
        if dropchance > 0 or itemDropchance > 0: print("\nhere's what you found:\n")
        if dropchance > 0:
            for _ in range(dropchance):
                dropped = generateEquip(player, enemy.name, round(math.log(enemy.MaxHP)*(player.level^2)), math.floor((enemy.STR + enemy.DEX + enemy.DEF + enemy.AGI)/3))
                player.heldarmors[dropped.name] = dropped 
                print(" + " + dropped.name) 
        dropList = []
        for each in items.values():
            if each.minLevel <= player.level:
                dropList.append(each)
        if itemDropchance > 0 and len(dropList) > 0:
            for _ in range(itemDropchance):
                randChoice = random.choice(dropList)
                incrementDict(randChoice, player.inventory, 1)
                print(f" + {randChoice.name}")
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
            if chosen == "HP":
                player.MaxHP += 3
                player.HP = player.MaxHP
                print("max HP increased by 3")
                print("HP fully restored!")
            elif chosen == "MP":
                player.MaxMP += 2
                player.MP = player.MaxMP
                print("max MP increased by 3")
                print("MP fully restored!")
            else:
                exec(f"player.{chosen} += {1}")
                print(f"{chosen} increased by 1")
            player.XP -= player.MaxXP
            player.MaxXP = round(player.MaxXP * 1.5)
            player.level += 1
        print("")  
    else:
        print("you were slain...")
        end = None
        while (end != "quit"):
            end = input("type 'quit' to quit the app\n> ")        
        quit()

# allows the player to heal, equip gear
def restSite(player: Entity):
    randchoice = random.choice(["campfire", "campsite", "clearing", "small ruin"])
    print("you come across a " + randchoice)
    print("you feel like this is a safe place for you to gather yourself.")
    print("")
    chosen = None
    while (True):
        chosen = verify("what will you do? [rest, equip, unequip, drop, leave]\n> ", ["rest", "equip", "unequip", "drop", "leave", "r", "e", "u", "d", "l"])
        if chosen == "rest" or chosen == "r":
            if player.HP >= player.MaxHP and player.MP >= player.MaxMP:
                print("you already feel rested, you don't feel the need to do so again right now")
            else:
                player.HP = player.MaxHP
                player.MP = player.MaxMP
                print("MP and HP fully restored!")
        elif chosen == "equip" or chosen == "e":
            print('\nyour equipment:\n')
            index = 0
            for key, value in player.heldarmors.items():
                print(f"{index}. {key} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = verify("\nwhat would you like to equip? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
            if select == 'back':                 
                continue
            elif select in player.heldarmors.keys():
                select = player.heldarmors.get(select)
                if player.equip.get(select.slot, None) != None:
                    toUnequip = player.equip.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    unequip(player, toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                equip(player, player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
            else:
                select = int(select)
                select = list(player.heldarmors.keys())[select]
                select = player.heldarmors.get(select)
                if player.equip.get(select.slot, None) != None:
                    toUnequip = player.equip.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    unequip(player, toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                equip(player, player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
        elif chosen == "unequip" or chosen == "u":
            for key, value in player.equip:
                print(f"{key}: {value.name} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
            select = verify("\nwhat slot would you like to unequip? type back to go back [weapon, helmet, chestplate, boots, charm] \n> ", ["weapon", "helmet", 'chestplate', 'boots', 'charm', 'back'])
            if select == "back":                 
                continue            
            select = player.equip.get(select)
            if select != None:
                print("you unequip the " + select.name)
                unequip(player, select.slot)
                player.heldarmors[select.name] = select
            else:
                print("you don't have anything to unequip there!")
        elif chosen == "drop" or chosen == "d":             
            print('\nyour equipment:\n')
            index = 0
            for key, value in player.heldarmors.items():
                print(f"{index}. {key} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = verify("\nwhat would you like to drop? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
            if select == 'back':                 
                continue
            elif select in player.heldarmors.keys():
                player.heldarmors.pop(select)
                print("\nyou dropped your " + select)
            else:
                select = int(select)
                select = list(player.heldarmors.keys())[select]
                player.heldarmors.pop(select)
                print("\nyou dropped your " + select)
            # input("\nenter anything to continue...\n> ")            
        elif chosen == "leave" or chosen == "l":
            print("you get up and get going\n")
            break

def doShop(player: Entity):
    class Buyable:
        def __init__(self, item: Item, cost: int):
            self.item = item
            self.name = self.item.name
            self.cost = cost
    stock = []
    stockNames = []
    for each in items.values():
        if each.minLevel <= player.level + 3:
            cost = math.ceil(((each.minLevel**1.3) / (player.level)) * max(min(round(random.normalvariate(12.5,1)), 15), 10) + max(min(round(random.normalvariate(0,2)), 5), -5))
            stock.append(Buyable(each, cost))
            stockNames.append(each.name)
    inquire = '\n"oh hi!" they say. "how can i help ya?" [buy, sell, leave]\n> '
    buyInquire = '\n"...what do you want to buy?" or type back to go back\n> '
    sellInquire = '\n"what exactly do ya wanna sell?" or back to go back\n> '
    armorCost = round(player.MaxHP * random.uniform(10,15))
    print('a little kobold traveling merchant waves to you, setting their massive backpack down')
    chosen = None
    while chosen != "leave" and chosen != "l":
        # ask if buying, selling, or leaving
        chosen = verify(inquire, ["buy", "sell", "leave", "b", "s", "l"])
        # main shop menu
        inquire = '\n"what else can i help ya with?" [buy, sell, leave]\n> '
        if chosen == "buy" or chosen == "b":
            # buy submenu
            subChosen = verify('\n"sure! what do ya wanna buy?" [items, equips, back]\n> ', ["items", "i", "back", "b", "equips", "e"])
            if subChosen == "back" or subChosen == "b":
                continue
            elif subChosen == "items" or subChosen == "i":
                # print item stock & costs
                print('''\n"okay! here's what i've got..."''')
                index = 0
                for each in stock:
                    print(f"{index}. {each.item.name}: {each.cost} gold")
                    index += 1
                # compile allowed list (index and item name)
                allowed = list(range(len(stock)))
                index1 = 0
                for each in allowed: 
                    allowed[index1] = str(each)
                    index1 += 1
                allowed += stockNames
                # get desired purchase
                item = None
                while item != "back":
                    item = verify(buyInquire, allowed + ["back"])
                    buyInquire = '\n"...what else do ya wanna get?" or type back to go back\n> '
                    if item.isdigit(): item = int(item)
                    if item == "back": continue
                    # if input is number, get stock's name
                    elif item not in stockNames: item = stock[int(item)]
                    elif item in stockNames: item = stock[stockNames.index(item)]
                    print(f'''\n"okay! that'll be {item.cost} gold, please!"''')
                    if player.gold < item.cost:
                        print('''"oh, you don't have enough... maybe sell me some stuff, or come back later, okay?"''')
                    else:
                        print('you hand over your gold')
                        print('''"great! here ya go!"''')
                        print(f" + {item.name}")
                        player.gold -= item.cost
                        incrementDict(item.item, player.inventory, 1)
            elif subChosen == "equips" or subChosen == "e":
                armorType = verify('\n"...okay! what kind of equipment?" [weapon, head, chestplate, boots, charm, back]\n> ', ['weapon', 'head', 'chestplate', 'boots', 'charm', 'back'])
                if armorType == "back": continue
                confirm = verify(f'''"sure! that'll be {armorCost} gold. all good?" [yes, no]\n> ''', ["yes", "no", 'y', 'n'])
                if confirm == 'n' or confirm == 'no': 
                    print('"awh."')
                    continue
                else:
                    if player.gold >= armorCost:
                        print('you hand over the gold, and the kobold digs into their backpack')
                        player.gold -= armorCost
                        print('''"let's see... here! this should fit you well."''')
                        generatedEquip = generateEquip(player, "self", round(player.MaxHP * random.uniform(0.5,0.75)), math.floor((player.STR + player.DEX + player.DEF + player.AGI)/3), 0, 0, armorType)
                        print('"here ya go!"')
                        print(f" + {generatedEquip.name}")
                        player.heldarmors[generatedEquip.name] = generatedEquip
                        armorCost = round(player.MaxHP * random.uniform(10,15))
                    else:
                        print('''"hey, you don't have enough money... maybe some other time?''')
        elif chosen == "sell" or chosen == "s":
            # buy submenu
            subChosen = verify('\n"sure! what do ya wanna sell?" [items, equips, back]\n> ', ["items", "i", "back", "b", "equips", "e"])
            if subChosen == "back" or subChosen == "b":
                continue
            elif subChosen == "items" or subChosen == "i":
                # print item inventory & sell price
                print('''\n"okay! what do ya have?"''')
                item = None
                while item != "back":
                    index = 0
                    playerSellList = []
                    allowed = []
                    for item in player.inventory.keys():
                        itemSellValue = math.ceil(stock[stockNames.index(item.name)].cost / 2)
                        print(f"{index}. {item.name}: {itemSellValue} gold ({player.inventory[item]})")
                        # create a list (playerSellList) of all of the items the player has and their sell values
                        playerSellList.append(Buyable(item, itemSellValue))
                        allowed.append(item.name)
                        index += 1
                    for each in range(len(allowed)): allowed.append(str(each))
                    allowed.append('back')
                    item = verify(sellInquire, allowed)
                    sellInquire = '\n"what else do ya wanna sell?" or back to go back\n> '
                    if item == "back":
                        continue
                    # fetch item object
                    if item.isdigit(): item = stock[stockNames.index(allowed[int(item)])]
                    else: item = stock[stockNames.index(item)]
                    # "item" is now saved as "Buyable" object
                    print(f'\n"okay, your {item.name} please!"')
                    if player.inventory[item.item] > 0:
                        print('you hand it over to the little kobold')
                        incrementDict(item.item, player.inventory, -1)
                        print('"thank you... and here you go!"')
                        print(f" + {item.cost} gold")
                    else:
                        print('''"oh, you're all out of those. that's okay!"\n''')
                    print("")
            elif subChosen == "equips" or subChosen == "e":
                print("lemme see your equipment, then!")
                pass
    print('''"awh... okay! i'll see you later, friend!"\nthey wave goodbye to you excitedly as you walk away\n''')

player = Entity("you", 20, 5, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery"], { }, 30)

#player = Entity("you", 999999, 999999, 3, 5, 0, 0, ["doublecut", "bolt", "warcry", "protection", "bravery", "bite", "nuke"], { }, 999999, [], ["player.MP = player.MaxMP\nprint('your MP was refilled')"])

doShop(player)
doCombat(player, "rat")
doCombat(player, "wolf")
doCombat(player, "wolf")
restSite(player)
print("your experience with fighting beasts have taught you something")
print("you learned the spell 'bite'!")
player.spells += ["bite"]
print("")
doCombat(player, "spirit")
doCombat(player, "spirit")
print("your experience with fighting spirits have taught you something")
print("you learned the spell 'cleanse'!")
player.spells += ["cleanse"]
print("")
doCombat(player, "imp")
doCombat(player, "imp")
doCombat(player, "demon")
doShop(player)
restSite(player)
print("your experience with fighting fiends have taught you something")
print("you learned the spells 'flame' and 'fireball'!")
player.spells += ["flame", "fireball"]
print("")
doCombat(player, "warg")
restSite(player)
doCombat(player, "reaper")
print("wowie.")