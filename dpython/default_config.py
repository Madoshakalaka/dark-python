oldprint = print

def print(s):
    oldprint('Pwned by Dark Python!! ', end='')
    oldprint(s)

