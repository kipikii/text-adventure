options = ["haha",'sad']

def verify(question):
    correct = False
    while (correct == False):
        chosen = input(question)
        for i in options:
            if (chosen == i):
                correct = True
                print(chosen)
    
verify('wawa? ')