import random, math, helpers, data

# allows the player to heal, equip gear
def restSite(player: data.Entity):
    randchoice = random.choice(["campfire", "campsite", "clearing", "small ruin"])
    print("you come across a " + randchoice)
    print("you feel like this is a safe place for you to gather yourself.")
    print("")
    chosen = None
    while (True):
        chosen = helpers.verify("what will you do? [rest, equip, unequip, drop, leave]\n> ", ["rest", "equip", "unequip", "drop", "leave", "r", "e", "u", "d", "l"])
        if chosen in ["rest", "r"]:
            if player.HP >= player.MaxHP and player.MP >= player.MaxMP:
                print("you already feel rested, you don't feel the need to do so again right now")
            else:
                player.HP = player.MaxHP
                player.MP = player.MaxMP
                print("MP and HP fully restored!")
        elif chosen in ["equip", "e"]:
            print('\nyour equipment:\n')
            index = 0
            for key, value in player.heldarmors.items():
                print(f"{index}. {key} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = helpers.verify("\nwhat would you like to equip? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
            if select == 'back':                 
                continue
            elif select in player.heldarmors.keys():
                select = player.heldarmors.get(select)
                if player.equipped.get(select.slot, None) != None:
                    toUnequip = player.equipped.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    player.unequip(toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                player.equip(player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
            else:
                select = int(select)
                select = list(player.heldarmors.keys())[select]
                select = player.heldarmors.get(select)
                if player.equipped.get(select.slot, None) != None:
                    toUnequip = player.equipped.get(select.slot)
                    print("you unequip your " + toUnequip.name)
                    player.unequip(toUnequip.slot)
                    player.heldarmors[toUnequip.name] = toUnequip
                print('you equip the ' + select.name)
                player.equip(player.heldarmors.get(select.name), select.slot)
                player.heldarmors.pop(select.name)
        elif chosen in ["unequip", "u"]:
            for key, value in player.equip:
                print(f"{key}: {value.name} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
            select = helpers.verify("\nwhat slot would you like to unequip? type back to go back [weapon, helmet, chestplate, boots, charm] \n> ", ["weapon", "helmet", 'chestplate', 'boots', 'charm', 'back'])
            if select == "back":                 
                continue            
            select = player.equipped.get(select)
            if select != None:
                print("you unequip the " + select.name)
                player.unequip(select.slot)
                player.heldarmors[select.name] = select
            else:
                print("you don't have anything to unequip there!")
        elif chosen in ["drop", "d"]:             
            print('\nyour equipment:\n')
            index = 0
            for key, value in player.heldarmors.items():
                print(f"{index}. {key} [{value.HP}, {value.MP}, {value.STR}, {value.DEX}, {value.DEF}, {value.AGI}]")
                index += 1
            weirdlist = list(range(len(player.heldarmors.keys())))
            weirdlist = [str(each) for each in weirdlist]
            select = helpers.verify("\nwhat would you like to drop? type back to go back\n> ", list(player.heldarmors.keys()) + ["back"] + weirdlist)
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

# gives the player a shop
def doShop(player: data.Entity):
    class Buyable:
        def __init__(self, item: data.Item, cost: int):
            self.item = item
            self.name = self.item.name
            self.cost = cost
    stock = []
    stockNames = []
    for each in data.items.values():
        if each.minLevel <= player.level + 3:
            cost = math.ceil(((each.minLevel**1.3) / (player.level)) * max(min(round(random.normalvariate(12.5,1)), 15), 10) + max(min(round(random.normalvariate(0,2)), 5), -5))
            stock.append(Buyable(each, cost))
            stockNames.append(each.name)
    inquire = '\n"oh hi!" they say. "how can i help ya?" [buy, sell, leave]\n> '
    buyInquire = '\n"...what do you want to buy?" or type back to go back\n> '
    sellInquire = '\n"what exactly do ya wanna sell?" or back to go back\n> '
    armorCost = round(player.level * 20 * max(min(round(random.normalvariate(12.5, 2)), 15), 10))
    print('a little kobold traveling merchant waves to you, setting their massive backpack down')
    chosen = None
    while chosen != "leave" and chosen != "l":
        # ask if buying, selling, or leaving
        chosen = helpers.verify(inquire, ["buy", "sell", "leave", "b", "s", "l"])
        # main shop menu
        inquire = '\n"what else can i help ya with?" [buy, sell, leave]\n> '
        if chosen in ["buy", "b"]:
            # buy submenu
            subChosen = helpers.verify('\n"sure! what do ya wanna buy?" [items, equips, back]\n> ', ["items", "i", "back", "b", "equips", "e"])
            if subChosen in ["back", "b"]:
                continue
            elif subChosen in ["items", "i"]:
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
                    item = helpers.verify(buyInquire, allowed + ["back"])
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
                        helpers.incrementDict(item.item, player.inventory, 1)
            elif subChosen in ["equips", "e"]:
                armorType = helpers.verify('\n"...okay! what kind of equipment?" [weapon, head, chestplate, boots, charm, back]\n> ', ['weapon', 'head', 'chestplate', 'boots', 'charm', 'back'])
                if armorType == "back": continue
                confirm = helpers.verify(f'''"sure! that'll be {armorCost} gold. all good?" [yes, no]\n> ''', ["yes", "no", 'y', 'n'])
                if confirm == 'n' or confirm == 'no': 
                    print('"awh."')
                    continue
                else:
                    if player.gold >= armorCost:
                        print('you hand over the gold, and the kobold digs into their backpack')
                        player.gold -= armorCost
                        print('''"let's see... here! this should fit you well."''')
                        generatedEquip = player.generateEquip(round(player.MaxHP * random.uniform(0.5,0.75)), math.floor((player.STR + player.DEX + player.DEF + player.AGI)/3), 0, 0, armorType)
                        print('"here ya go!"')
                        print(f" + {generatedEquip.name}")
                        player.heldarmors[generatedEquip.name] = generatedEquip
                        armorCost = round(player.MaxHP * random.uniform(10,15))
                    else:
                        print('''"hey, you don't have enough money... maybe some other time?''')
        elif chosen in ["sell", "s"]:
            # buy submenu
            subChosen = helpers.verify('\n"sure! what do ya wanna sell?" [items, equips, back]\n> ', ["items", "i", "back", "b", "equips", "e"])
            if subChosen in ["back", "b"]:
                continue
            elif subChosen in ["items", "i"]:
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
                    item = helpers.verify(sellInquire, allowed)
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
                        helpers.incrementDict(item.item, player.inventory, -1)
                        print('"thank you... and here you go!"')
                        print(f" + {item.cost} gold")
                    else:
                        print('''"oh, you're all out of those. that's okay!"\n''')
                    print("")
            elif subChosen in ["equips", "e"]:
                print('"lemme see your equipment, then!"')
                item = None
                while item != "back":
                    index = 0
                    playerSellList = []
                    allowed = []
                    for item in player.heldarmors.keys():
                        armor = player.heldarmors[item]
                        itemSellValue = math.ceil((armor.HP + armor.MP + armor.STR + armor.DEX + armor.DEF + armor.AGI) * 1.5)
                        print(f"{index}. {item}: {itemSellValue} gold")
                        # create a list (playerSellList) of all of the equipment the player has and their sell values
                        playerSellList.append(Buyable(armor, itemSellValue))
                        allowed.append(item)
                        index += 1
                    for each in range(len(allowed)): allowed.append(str(each))
                    allowed.append('back')
                    item = helpers.verify(sellInquire, allowed)
                    sellInquire = '\n"what else do ya wanna sell?" or back to go back\n> '
                    if item == "back":
                        continue
                    # fetch item object
                    if item.isdigit(): item = playerSellList[int(item)]
                    else: item = playerSellList[allowed.index(item)]
                    # "item" is now saved as "Buyable" object
                    print(f'\n"okay, your {item.name} please!"')
                    if item.name in player.heldarmors:
                        print('you hand it over to the little kobold')
                        player.heldarmors.pop(item.name)
                        print('"thank you... and here you go!"')
                        print(f" + {item.cost} gold")
                        player.gold += item.cost
                    else:
                        print('''"well, you don't have that... uhm, maybe something else?"\n''')
                    print("")
    print('''"awh... okay! i'll see you later, friend!"\nthey wave goodbye to you excitedly as you walk away\n''')
