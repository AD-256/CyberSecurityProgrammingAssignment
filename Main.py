import re
import _mysql_connector
import functions

functions.ynInput()

passwordAttempt = input()

if re.search(".{13,}",passwordAttempt):#Strong
    print("Strong")
elif re.search("",passwordAttempt):#Weak
    print("weak")
else :#Invalid
    print("inv")