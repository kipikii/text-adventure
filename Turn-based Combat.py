# Held items stored in this list
inventory = []
# Equipped order: Weapon, Armor, Charm (accessory)
equipped = ['None', 'None', 'None']
# Options that the player can make at this time
valid = []

def action():
    pass

def verify(question):
    correct = False
    while (correct == False):
        chosen = input(question)
        for i in valid:
            if (chosen == i):
                correct = True
                print(chosen)

print('You wake up in the middle of the woods.')
print('You do not recognize any of your surroudings, though a silver dagger nearby catches your eye. [dagger]')
valid.append('dagger')
print('The vast forest in front of you beckons you... [onward]')
print('Your options:')
for i in valid:
    print(i)
