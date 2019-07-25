oldprint = print

def print(x):
    oldprint(x+1)