playerHP = 15
playerSTR = 5
playerDEX = 5
playerCharm = None
enemyHP = 15
enemyATK = 5
enemyDEX = 5

valid = ["attack", "skill", "item", "run"]

def fight():
    pass

def verify(question):
    correct = False
    while (correct == False):
        chosen = input(question)
        for i in valid:
            if (chosen == i):
                correct = True
                print(chosen)

def doCombat(playerHP, playerSTR, playerDEX, playerCharm, enemyName, enemyHP, enemyATK, enemyDEX):
    print("A " + enemyName + " appeared!")
    verify("What would you like to do? [attack, skill, item, run] ")

doCombat(playerHP, playerSTR, playerDEX, playerCharm, "wolf", enemyHP, enemyATK, enemyDEX)