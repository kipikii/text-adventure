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
    #"giant spider": [30, 3, 6, 3],
    #"baslisk": [40, 7, 0, 5]
}

inventory = {
    # "item": quantity
    "small potion of healing": 3,
    "throwing knife": 2
}

# player's placeholder stats
playerHP = 15
playerMaxHP = playerHP
playerSTR = 2
playerDEX = 1
playerDEF = 0
playerCharm = None

battlevalid = ["attack", "skill", "item", "a", "s", "i", None]

skills = [ ]

def verify(question, allowed):
    while (True):
        if (question == None):
            chosen = input("what will you do? ")
        else:
            chosen = input(question)
        for i in allowed:
            if (chosen == i):
                return chosen

def doCombat(enemyName):
    enemyHP = stats[0]
    enemySTR = stats[1]
    enemyDEX = stats[2]
    enemyDEF = stats[3]

    global inventory, playerHP, playerSTR, playerDEX, playerDEF, playerCharm

    print("a " + enemyName + " appeared")
    # run routine while both sides are alive
    while (playerHP > 0 and enemyHP > 0):
        print("[Your HP: " + str(playerHP) + " / " + str(playerMaxHP) + "]")
        chosen = verify("what would you like to do? [attack, skill, item] ", battlevalid)

        # code for attacking
        if (chosen == "attack" or chosen == "a" or chosen == None):
            # get the percentage chance for the player to hit
            if (enemyDEX == 3):
                hitChance = round(log((playerDEX * (2.999999 / (enemyDEX + .0000001)))) * 40)
            else:
                hitChance = round(log((playerDEX * (3 / (enemyDEX + .0000001)))) * 40)
            print(hitChance)
            if (hitChance < 30):
                hitChance = 30
            if (hitChance >= randint(1,100)):
                damage = round((playerSTR - enemyDEF) * (randint(90, 110)/100))
                if (damage >= 0):
                    print("you attacked the " + enemyName + " for " + str(damage) + " damage")
                    enemyHP -= damage
                else:
                    print("you attacked the " + enemyName + " for 0 damage")
            else:
                print("your attack missed")

        # code for using skills
        elif (chosen == "skill" or chosen == "s"):
            print("i'm definitely going to add skills")

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
            index = None
            print(" ")
            chosen = verify("choose an item to use: ", invKeys)
            print("you used a " + chosen)
            if (chosen == "small potion of healing"):
                healAmount = randint(5, 10)
                playerHP += healAmount
                if (playerHP > playerMaxHP):
                    playerHP = playerMaxHP
                print("the small potion revitalizes you, healing you for " + str(healAmount) + " [" + str(playerHP) + "/" + str(playerMaxHP) + "]")
                healAmount = None
                inventory.update({"small potion of healing": (inventory["small potion of healing"] - 1)})
                if (inventory["small potion of healing"] <= 0):
                    inventory.pop("small potion of healing")
                
            elif (chosen == "throwing knife"):
                damage = playerDEX + playerSTR
                if (damage < 0):
                    damage = 0
                print("you chuck the throwing knife at the " + enemyName + ", dealing " + str(damage) + " damage")
                enemyHP -= damage
                damage = None
                inventory.update({"throwing knife": (inventory["throwing knife"] - 1)})
                if (inventory["throwing knife"] <= 0):
                    inventory.pop("throwing knife")

        # if the enemy is alive, have them attack
        if (enemyHP > 0):
            print(" ")
            print("the " + enemyName + " attacks")
            if (playerDEX == 3):
                hitChance = round(log((enemyDEX * (2.999999 / (enemyDEX + .0000001)))) * 40) + 30
            else:
                hitChance = round(log((enemyDEX * (3 / (enemyDEX + .0000001)))) * 40) + 30
            print(hitChance)
            if (hitChance >= randint(1,100)):
                damage = round((enemySTR - playerDEF) * (randint(90, 110)/100))
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
    playerHP += 1
    playerMaxHP += 1
    playerSTR += 1
    playerDEX += 1
    playerDEF += 1
    print("as you defeat the beast, another creature leaps out at you")
