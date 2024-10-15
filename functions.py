import re
def ynInput():
    if re.search("[yY]",input()) != None: return True
    else: return False