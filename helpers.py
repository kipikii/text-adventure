import random, data
from data import player

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
            print("~~~~~~~~~~")
            if chosen == "/help":
                print("valid commands:")
                print("/help - displays this menu")
                print("/stats - displays your current stats")
                print("/inventory || /inv - shows your inventory and gold")
                print("/spell <spellName> - gives you information regarding the spell provided")
                print("/item <itemName> - gives you information regarding the item provided")
                print("/credits - the beautiful people who worked on this game")
                print("/quit - quits the game")
                print("/patchnotes - shows the patch notes")
            elif chosen == "/stats":
                global player
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
            elif chosen == "/patchnotes":
                print("patch notes:")
                print("v1.0 - initial release")
                print("v1.1 - added a working shop and a working /patchnotes command")
            elif chosen == "/quit":
                print("bye!")
                quit()
            elif chosen == "/inventory" or chosen == "/inv":
                print(f"your gold: {player.gold}")
                print ("\nequipped:")
                for eachKey, val in player.equipped.items():
                    if val is None:
                        print(f"{eachKey}: none")
                        continue
                    print(f"{eachKey}: {val.HP} HP, {val.MP} MP, {val.STR} STR, {val.DEX} DEX, {val.DEF} DEF, {val.AGI} AGI")
                print("\nyour items:")
                if not player.inventory:
                    print("none")
                else:
                    for eachKey, eachValue in player.inventory.items():
                        print(f"{eachKey.name}: {eachValue}")
                print("")
                print("your equips:")
                if not player.heldarmors:
                    print("none")
                else:
                    for key, value in player.heldarmors.items(): 
                        print(f"{key}: [{value.HP} HP, {value.MP} MP, {value.STR} STR, {value.DEX} DEX, {value.DEF} DEF, {value.AGI} AGI]")
            elif chosen == "/credits":
                print("")
                print("kip semos - main developer")
                # don't ask, they asked for this
                if random.randint(1,2) == 1:
                    print("jaxon tran - one of the only people who can understand my code and resident crazy idea man")
                    print("odin simonson - can understand my code and professional patch notes enjoyer")
                else:
                    print("odin simonson - can understand my code and professional patch notes enjoyer")
                    print("jaxon tran - one of the only people who can understand my code and resident crazy man")
                print("")
            elif "/spell " in chosen:
                spellName = chosen.removeprefix("/spell ")
                if spellName in data.spells.keys():
                    print(f"\n{spellName.capitalize()}:\n- {data.spells[spellName].description}\n")
                else:
                    print("invalid spell name.")
            elif "/item " in chosen:
                itemName = chosen.removeprefix("/item ")
                if itemName in data.items.keys():
                    print(f"\n{itemName.capitalize()}:\n- {data.items[itemName].description}\n")
                else:
                    print("invalid item name.")
            else:
                print("invalid command. to see all valid commands, do /help")
            print("~~~~~~~~~~")
        for i in allowed:
            if isinstance(i, str): i = i.lower()
            if chosen == i:
                return chosen

# for dictionaries where the key's values are only numbers *wink wink inventory*
def incrementDict(item:data.Item, given:dict, change:int=1):
    if item in list(given.keys()):
        given[item] = (given.get(item)) + change
    else:
        given[item] = change
    if given[item] <= 0:
        given.pop(item)
    return given
