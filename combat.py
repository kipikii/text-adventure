from random import *
from time import *

# list of monsters you can fight
monsters = {
    # stats go [hp, str, dex, def]
    "wolf": [10, 2, 3, 0],
    "rat": [3, 1, 0, 0],
    "god": [999, 99, 99, 99]
}

inventory = {
    # "item": quantity
    "weak potion of healing": 3,
    "throwing knife": 2
}

# change below string to change what monster you fight
enemyName, stats = choice(list(monsters.items()))
enemyHP = stats[0]
enemySTR = stats[1]
enemyDEX = stats[2]
enemyDEF = stats[3]

playerHP = 15
playerMaxHP = playerHP
playerSTR = 5
playerDEX = 2
playerDEF = 0
playerCharm = None

valid = ["attack", "skill", "item"]

def verify(question):
    while (True):
        if (question == None):
            chosen = input("what will you do? ")
        else:
            chosen = input(question)
        for i in valid:
            if (chosen == i):
                return chosen

def doCombat(playerHP, playerSTR, playerDEX, playerDEF, playerCharm, enemyName, enemyHP, enemySTR, enemyDEX, enemyDEF):
    print("a " + enemyName + " appeared!")
    # run routine while both sides are alive
    while (playerHP > 0 and enemyHP > 0):
        print("[Your HP: " + str(playerHP) + " / " + str(playerMaxHP) + "]")
        chosen = verify("what would you like to do? [attack, skill, item] ")
        # code for attacking
        if (chosen == "attack"):
            # get the percentage chance for the player to hit
            hitChance = round(playerDEX / (enemyDEX + 1) * 100)
            if (hitChance >= randint(1,100)):
                print("you attacked the " + enemyName + " for " + str(playerSTR - enemyDEF) + " damage")
                enemyHP -= playerSTR - enemyDEF
            else:
                print("your attack missed")

        # code for using skills
        elif (chosen == "skill"):
            print("i'm definitely going to add skills")

        # code for using items
        elif (chosen == "item"):
            print("inventory here or smth")

        # if the enemy is alive, have them attack
        if (enemyHP > 0):
            print(" ")
            print("the " + enemyName + " attacks")
            hitChance = round(enemyDEX / (playerDEX + 1) * 100)
            if (hitChance >= randint(1,100)):
                print("you took " + str(enemySTR - playerDEF) + " damage")
                playerHP -= enemySTR - playerDEF
            else:
                print("but its attack missed")
        if (enemyHP > 0):
            print(" ")
    # figure out who's alive at the end of the fight
    if (enemyHP <= 0):
        print("the " + enemyName + " has been slain")
    else:
        print("you were slain...")
        quit()

# forever fight creatures
while (True):
    doCombat(playerHP, playerSTR, playerDEX, playerDEF, playerCharm, enemyName, enemyHP, enemySTR, enemyDEX, enemyDEF)
    print(" ")
    print("as you defeat the beast, another creature leaps out at you")
    enemyName, stats = choice(list(monsters.items()))
    enemyHP = stats[0]
    enemySTR = stats[1]
    enemyDEX = stats[2]
    enemyDEF = stats[3]
