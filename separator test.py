def separator(statuses:list, toRemove):
    statusIndex = statuses.index(toRemove)
    firstHalf = statuses[:statusIndex]
    print(firstHalf)
    secondHalf = statuses[statusIndex:]
    secondHalf.pop(0)
    for each in secondHalf:
        # applyStatus(status, victim, True) here
        firstHalf.append(each)
    return firstHalf
    


separateThis = ["thing 1", "thing 2", "thing 3", "thing 4", "thing 5", "thing 6", "thing 7"]

print(separator(separateThis, "thing 5"))