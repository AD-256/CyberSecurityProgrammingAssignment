import re
import sqlite3
import functions

userDataDB = sqlite3.connect("userData.db")

print ("Would you like to ")
functions.ynInput()

print("Input your new password")
passwordAttempt = input()

if re.search(".{13,}",passwordAttempt):#Strong
    print("Strong")
elif re.search("",passwordAttempt):#Weak
    print("weak")
else :#Invalid
    print("inv")