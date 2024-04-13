# Held items stored in this list
inventory = []
# Equipped order: Weapon, Armor, Charm (accessory)
equipped = ['None', 'None', 'None']
# Options that the player can make at this time
valid = []
worldType = 'overworld'

def verify(action):
    for potential in valid:
        if (action == potential):
            return action
        else:
            return 'invalid'

print('You wake up in the middle of the woods.')
print('You do not recognize any of your surroudings, though a bronze shortsword nearby catches your eye. [shortsword]')
valid.append('shortsword')
print('You feel that you have almost no other options other than to just venture onwards. [onward]')
valid.append('onward')
print('Your options:')
for i in valid:
    print(i)
action = input('What do you do? ')
verify(action)
if (action == 'invalid'):
    input('That command is invalid. Try again. ')
