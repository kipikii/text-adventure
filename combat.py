import math, random, copy, helpers, data

def castSpell(spell:data.Spell, caster:data.Entity, victim:data.Entity):
    spell = data.spells[spell]
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
            if damage <= 0 and (spell.hitStat != math.inf or spell.hitStat != 0):
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
            hitChance = round(math.log(attackerHit * (2.999999 / (victimDodge + 0.0000001))) * 40  ) + 50
        else: 
            hitChance = round(math.log((attackerHit) * (3 / (victimDodge + 0.0000001))) * 40) + 50
    if hitChance < 30: hitChance = 30
    if hitChance >= random.randint(1,100): return True
    else: return False

# causes a combat to initate between two entities
def doCombat(player: data.Entity, enemy: data.Entity):  
    enemy = copy.copy(data.monsters[enemy])
    print("a " + enemy.name + " appeared!")
    while (player.HP > 0 and enemy.HP > 0):
        for each in player.onTurnStart:
            each = "data.player." + each
            exec(each)
        print("[Your HP: " + str(player.HP) + " / " + str(player.MaxHP) + "] [Your MP: " + str(player.MP)+ " / " + str(player.MaxMP) + "]")
        chosen = helpers.verify("what would you like to do? [attack, spell, item, pass]\n> ", ["attack", "spell", "skill", "item", "pass", "a", "s", "i", "p"])
        print("")
        # player uses attack action (secretly just a free spell)
        if chosen in ["a", "attack"]:
            castSpell("attack", player, enemy)
            # proc on attack abilities
            for each in player.onAttack:
                exec(each)
        # player casts spell
        elif chosen in ["spell", "skill", "s"]:
            # list player's spells
            print("your spells:")
            index = 0
            for each in player.spells:
                each = data.spells[each]
                print(f"{index}. {each.name}: {each.cost} MP")
                index += 1
            weirdlist = list(range(len(player.spells)))
            weirdlist = [str(each) for each in weirdlist]
            allowed = player.spells + ["back"] + weirdlist
            # let the player choose a spell to cast
            chosen = helpers.verify("\nchoose a spell to cast, or type back to go back\n> ", allowed)
            # player wants to go back
            if chosen == "back":
                # restart loop (player chooses action again)
                continue
            # player casts a spell
            else:
                if chosen not in player.spells:
                    chosen = player.spells[int(chosen)]
                # check for enough MP
                if data.spells[chosen].cost <= player.MP:
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
        elif chosen in ["item", "i"]:
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
            chosen = helpers.verify("\nchoose an item to use, or type back to go back\n> ", allowed)
            if chosen == "back": continue
            else:
                if chosen.isdigit(): chosen = allowed[int(chosen)]
                usedItem = data.items[chosen]
                exec(usedItem.code)
                helpers.incrementDict(usedItem, player.inventory, -1)
                if player.HP > player.MaxHP: player.HP = player.MaxHP
                if player.MP > player.MaxMP: player.MP = player.MaxMP
        elif chosen == "pass" or chosen == "p":
            print("you wait")    
        # proc all of the player's status effects
        for each in player.status:
            player.tickStatus(each, enemy.HP > 0)
        # regenerate 1 mana for each 10 max mana the player has
        if not math.isinf(player.MP): player.MP += math.ceil(player.MaxMP / 10)
        if player.MP > player.MaxMP: player.MP = player.MaxMP
        # if the enemy is alive:    
        if enemy.HP > 0:
            # proc enemy's turn start abilities
            for each in enemy.onTurnStart:
                each = "enemy." + each
                exec(each)
            print("")
            # enemy casts a random spell from their spell list
            castSpell(random.choice(enemy.spells), enemy, player)
            # proc enemy's on attack abilities
            for each in enemy.onAttack:
                exec(each)
            # proc all of its status effects
            for each in enemy.status:
                enemy.tickStatus(each)
    if player.HP > 0:
        # remove statuses from player in reverse order
        (player.status).reverse()
        for each in player.status:
            player.removeStatus(each, True)
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
        for each in player.equipped.values():
            if each != None:
                numEquipped += 1
        if dropchance < 1 and numEquipped <= 1: dropchance = 1
        if dropchance > 0 or itemDropchance > 0: print("\nhere's what you found:\n")
        if dropchance > 0:
            for _ in range(dropchance):
                dropped = enemy.generateEquip(player)
                player.heldarmors[dropped.name] = dropped 
                print(" + " + dropped.name) 
        dropList = []
        for each in data.items.values():
            if each.minLevel <= player.level:
                dropList.append(each)
        if itemDropchance > 0 and len(dropList) > 0:
            for _ in range(itemDropchance):
                randChoice = random.choice(dropList)
                helpers.incrementDict(randChoice, player.inventory, 1)
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
            chosen = helpers.verify("pick a stat to increase [HP, MP, STR, DEX, DEF, AGI]\n> ", ["HP", "MP", "STR", "DEX", "DEF", "AGI"])
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
