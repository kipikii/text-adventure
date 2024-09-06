valid = []

def verify(question):
    while (True):
        if (question == None):
            chosen = input("what will you do? ")
        else:
            chosen = input(question)
        for i in valid:
            if (chosen == i):
                return chosen

def forestOpening():
    from events import valid
    print('you wake up in the middle of the woods.')
    print('you do not recognize any of your surroudings, though a rusted dirk nearby catches your eye. [dirk]')
    valid.append("dirk")
    print('the vast forest in front of you beckons you. [onward]')
    valid.append('onward')
    chosen = verify()
    if (chosen == "dirk"):
        print("you picked up the small knife and placed it in your bag.")
        print("you see no more points of interest nearby, the dark forest ahead calling to you. [onward]")
        valid = ["onward"]
        chosen = verify()
    if (chosen == "onward"):
        print("you ventured deeper into the woods.")