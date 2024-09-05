valid = []

def verify():
    while (True):
        chosen = input("What will you do? ")
        for i in valid:
            if (chosen == i):
                return chosen

def forestOpening():
    from events import valid
    print('You wake up in the middle of the woods.')
    print('You do not recognize any of your surroudings, though a rusted dagger nearby catches your eye. [dagger]')
    valid.append("dagger")
    print('The vast forest in front of you beckons you... [onward]')
    valid.append('onward')
    chosen = verify()
    if (chosen == "dagger"):
        print("You picked up the dagger and placed it in your bag.")
        print("You see no more points of interest nearby, the dark forest ahead calling to you. [onward]")
        valid = ["onward"]
        chosen = verify()
    if (chosen == "onward"):
        print("You ventured deeper into the woods.")