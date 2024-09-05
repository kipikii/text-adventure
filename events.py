valid = []

def verify(question):
    while (True):
        chosen = input(question)
        for i in valid:
            if (chosen == i):
                return chosen

def forest():
    print('You wake up in the middle of the woods.')
    print('You do not recognize any of your surroudings, though a rusted dagger nearby catches your eye. [dagger]')
    valid.append('dagger')
    print('The vast forest in front of you beckons you... [onward]')
    valid.append('onward')
    print('Your options:')
    for i in valid:
        print(i)
    chosen = verify("What will you do? ")
    if (chosen == "dagger"):
        print("You picked up the dagger and placed it in your bag.")
    if (chosen == "onward"):
        print("You ventured deeper into the woods.")