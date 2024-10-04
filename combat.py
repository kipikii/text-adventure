from random import *
from time import *
from math import *

# list of monsters you can fight
monsters = {
    # stats go [hp, str, dex, def]
    # dex should be >= 0
    "wolf": [7, 2, 2, 0],
    "rat": [3, 1, 0, 0],
    "imp": [25, 2, 5, -3],
}

inventory = {
    # "item": quantity
    "small healing potion": 1
}

skills = {
    # "skill": mana cost
    "double cut": 2
}

# player's placeholder stats
playerMaxHP = 10
playerHP = playerMaxHP
playerMaxMana = 5
playerMana = playerMaxMana
playerSTR = 2
playerDEX = 1
playerDEF = 0
playerCharm = None

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

def changeInventory(item:str=None, change:int=-1):
    if (item == None):
        print("no item given to changeInventory, returned statement")
        return
    global inventory
    if (item in list(inventory.keys())):
        inventory[item] = (inventory.get(item)) + change
    else:
        inventory[item] = change
    if (inventory[item] <= 0):
        inventory.pop(item)

def checkMana(skill:str=None):
    global skills, playerMana
    if (skill == None):
        print("no skill supplied to checkMana, returning function")
        return False
    if playerMana >= skills[skill]:
        return True
    else:
        return False

def hitCalc(attackerDEX:int=0, victimDEX:int=0):
    if (victimDEX == 3):
        hitChance = round(log(((attackerDEX + 1) * (2.999999 / (victimDEX + 1.0000001)))) * 40) + 20
    else:
        hitChance = round(log(((attackerDEX + 1) * (3 / (victimDEX + 1.0000001)))) * 40) + 20
    if (hitChance < 30):
        hitChance = 30
    if (hitChance >= randint(1,100)):
        return "hit"
    else:
        return "miss"

def doCombat(enemyName:str=None):
    if (enemyName == None):
        enemyName = "god"
        enemyHP = 1500
        enemySTR = 100
        enemyDEX = 100
        enemyDEF = 100
        print("whoops, no enemy name. here's a god fight")
    else:
        enemyHP = stats[0]
        enemySTR = stats[1]
        enemyDEX = stats[2]
        enemyDEF = stats[3]

    global inventory, skills, playerHP, playerMana, playerSTR, playerDEX, playerDEF, playerCharm

    status = []

    print("a " + enemyName + " appeared")
    # run routine while both sides are alive
    while (playerHP > 0 and enemyHP > 0):
        print("[Your HP: " + str(playerHP) + " / " + str(playerMaxHP) + "] [Your mana: " + str(playerMana)+ " / " + str(playerMaxMana) + "]")
        chosen = verify("what would you like to do? [attack, skill, item] ", ["attack", "skill", "item", "a", "s", "i"])

        # code for attacking
        if (chosen == "attack" or chosen == "a"):
            # get the percentage chance for the player to hit
            if (hitCalc(playerDEX, enemyDEX) == "hit"):
                damage = round((playerSTR * (randint(90, 120)/100)) - enemyDEF)
                if (damage >= 0):
                    print("you attacked the " + enemyName + " for " + str(damage) + " damage")
                    enemyHP -= damage
                else:
                    print("you attacked the " + enemyName + " for 0 damage")
            else:
                print("your attack missed")
        # code for using skills
        elif (chosen == "skill" or chosen == "s"):
            print(" ")
            print("your skills:")
            for each in list(skills.keys()):
                print(each + ": " + str(skills[each]))
            allowed = list(skills.keys()) + ["back"]
            chosen = verify("choose an skill to use, or type back to go back: ", allowed)
            if (chosen == "back"):
                print(" ")
                continue
            else:
                if (checkMana(chosen) == False):
                    print("insufficent mana")
                    continue
                playerMana -= skills[chosen]
# double cut, attack twice
                if (chosen == "double cut"):
                    if (hitCalc(playerDEX + 2, enemyDEX)):
                        for each in range(2):
                            damage = round((playerSTR * (randint(100, 150)/100)) - enemyDEF)
                            if (damage >= 0):
                                print("you attacked the " + enemyName + " for " + str(damage) + " damage")
                                enemyHP -= damage
                            else:
                                print("you attacked the " + enemyName + " for 0 damage")
                    else:
                        print("your attack missed")
                else:
                    print("whoops, forgot to code that skill")
                    continue
        # code for using items
        elif (chosen == "item" or chosen == "i"):
            print(" ")
            print("your inventory:")
            invKeys = list(inventory.keys())
            invValues = list(inventory.values())
            index = 0
            for each in invKeys:
                print(each + ": " + str(invValues[index]))
                index += 1
            print(" ")
            allowed = invKeys + ["back"]
            chosen = verify("choose an item to use, or type back to go back: ", allowed)
            if (chosen == "back"):
                print(" ")
                continue
#small healing potion
            if (chosen == "small healing potion"):
                healAmount = randint(5, 15) / 100
                healAmount = ceil(healAmount * playerMaxHP)
                playerHP += healAmount
                if (playerHP > playerMaxHP):
                    playerHP = playerMaxHP
                print("drinking the potion revitalizes you, healing you for " + str(healAmount) + " [" + str(playerHP) + "/" + str(playerMaxHP) + "]")
                changeInventory(chosen, -1)
#throwing knife
            elif (chosen == "throwing knife"):
                damage = playerDEX + playerSTR
                if (damage < 0):
                    damage = 0
                print("you chuck the throwing knife at the " + enemyName + ", dealing " + str(damage) + " damage")
                enemyHP -= damage
                damage = None
                changeInventory(chosen, -1)
#small mana potion
            elif (chosen == "small mana potion"):
                healAmount = randint(5, 15) / 100
                healAmount = ceil(healAmount * playerMaxMana)
                if (playerMana > playerMaxMana):
                    playerMana = playerMaxMana
                print("drinking the potion gives you energy, regenerating " + str(healAmount) + " [" + str(playerMana) + "/" + str(playerMaxMana) + "]")
                healAmount = None
                changeInventory(chosen, -1)
            else:
                print("whoops, forgot to code that skill")
                continue

        # if the enemy is alive, have them attack
        if (enemyHP > 0):
            print(" ")
            print("the " + enemyName + " attacks")
            if (hitCalc(enemyDEX, playerDEX) == "hit"):
                damage = round((enemySTR * (randint(100, 150)/100)) - playerDEF)
                if (damage >= 0):
                    print("you took " + str(damage) + " damage")
                    playerHP -= damage
                else:
                    print("you took 0 damage")
            else:
                print("but its attack missed")
            print(" ")
    # figure out who's alive at the end of the fight
    if (enemyHP <= 0):
        print("the " + enemyName + " has been slain")
    else:
        print("you were slain...")
        quit()

# forever fight creatures
while (True):
    # get a random enemy's name and stats from the "monsters" dictionary
    enemyName, stats = choice(list(monsters.items()))
    doCombat(enemyName)
    print(" ")
    print("you became slightly stronger")
    playerHP += 1
    playerMaxHP += 1
    playerMana += 1
    playerMaxMana += 1
    playerSTR += 1
    playerDEX += 1
    playerDEF += 1
    if (randint(1,5) == 1):
        itemToAdd = choice(["throwing knife", "small healing potion", "small mana potion"])
        print("you found the " + enemyName + " was carrying a " + itemToAdd)
        print("you added the " + itemToAdd +" to your bag")
        changeInventory(itemToAdd, 1)
        print(" ")
    if (playerMaxHP > 20):
        monsters["giant spider"] = [30, 3, 6, 3]
        monsters["baslisk"] = [40, 7, 0, 5]
    print("as you defeat the beast, another creature leaps out at you")
    if (playerMaxHP >= 100 and randint(1,4) == 1):
        print("pick on someone your own size!")
        doCombat()
        print("oh wow you actually killed it. good job i guess.")
        quit()  