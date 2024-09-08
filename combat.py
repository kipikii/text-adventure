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

playerHP = 15
playerMaxHP = playerHP
playerSTR = 5
playerDEX = 2
playerDEF = 0
playerCharm = None

valid = ["attack", "skill", "item", "a", "s", "i"]

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
        if (chosen == "attack" or chosen == "a"):
            # get the percentage chance for the player to hit
            hitChance = round(playerDEX / (enemyDEX + 1) * 100) + 10
            if (hitChance >= randint(1,100)):
                damage = round((playerSTR - enemyDEF) * (randint(80, 120)/100))
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
            print("inventory here or smth")

        # if the enemy is alive, have them attack
        if (enemyHP > 0):
            print(" ")
            print("the " + enemyName + " attacks")
            hitChance = round(enemyDEX / (playerDEX + 1) * 100) + 10
            if (hitChance >= randint(1,100)):
                damage = round((enemySTR - playerDEF) * (randint(80, 120)/100))
                if (damage >= 0):
                    print("you took " + str(damage) + " damage")
                    playerHP -= damage
                else:
                    print("you took 0 damage")
            else:
                print("but its attack missed")
        if (enemyHP > 0):
            print(" ")
    # figure out who's alive at the end of the fight
    if (enemyHP <= 0):
        print("the " + enemyName + " has been slain")
        return playerHP
    else:
        print("you were slain...")
        quit()

# forever fight creatures
while (True):
    # get a random enemy's name and stats from the "monsters" dictionary
    enemyName, stats = choice(list(monsters.items()))
    enemyHP = stats[0]
    enemySTR = stats[1]
    enemyDEX = stats[2]
    enemyDEF = stats[3]
    playerHP = doCombat(playerHP, playerSTR, playerDEX, playerDEF, playerCharm, enemyName, enemyHP, enemySTR, enemyDEX, enemyDEF)
    print(" ")
    print("as you defeat the beast, another creature leaps out at you")
