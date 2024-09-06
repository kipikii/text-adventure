# list of monsters you can fight
monsters = {
    # stats go [name, hp, str, dex, def]
    "wolf": ["wolf", 10, 2, 2, 0],
    "rat": ["rat", 3, 1, 0, 0]
}

# change below string to change what monster you fight
enemy = monsters.get("rat")
enemyName = enemy[0].capitalize()
enemyHP = enemy[1]
enemySTR = enemy[2]
enemyDEX = enemy[3]
enemyDEF = enemy[4]

playerHP = 15
playerMaxHP = playerHP
playerSTR = 5
playerDEX = 5
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
        # code for dealing damage through attacking
        if (chosen == "attack"):
            print("you attacked the " + enemyName + " for " + str(playerSTR - enemyDEF) + " damage")
            enemyHP -= playerSTR - enemyDEF
        # code for using skills
        elif (chosen == "skill"):
            print("i'm definitely going to add skills")
        # code for using items
        elif (chosen == "item"):
            print("inventory here or smth")
        # if the enemy is alive, have them attack
        if (enemyHP > 0):
            print("the " + enemyName + " attacks!")
            print("you took " + str(enemySTR - playerDEF) + " damage")
        playerHP -= enemySTR - playerDEF
    # figure out who's alive at the end of the fight
    if (enemyHP <= 0):
        print("the " + enemyName + " has been slain.")
    else:
        print("you were slain...")

doCombat(playerHP, playerSTR, playerDEX, playerDEF, playerCharm, "wolf", enemyHP, enemySTR, enemyDEX, enemyDEF)
