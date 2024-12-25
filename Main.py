import re, sqlite3, magics, bcrypt

userDataDB = sqlite3.connect("userData.txt")
regexStrong = re.compile(r"(?=.{13,})(?=(.*[a-z]){2,})(?=(.*[A-Z]){2,})(?=(.*\d){2,})(?=(.*[^\w\d\s@#]){2,}).*$", re.MULTILINE | re.UNICODE)
regexWeak = re.compile(r"(?=.{8,})(?=(.*[a-z]){1,})(?=(.*[A-Z]){1,})(?=(.*\d){1,})(?=(.*[^\w\d\s@#]){1,}).*$", re.MULTILINE | re.UNICODE)

print ("Are you logging in?")
loginCheck = magics.ynInput()

if loginCheck == True:
    pass
elif loginCheck == False:
    print("Input your new username")
    userNameInput = str(input())
    print("Input your new password")
    passwordAttempt = input()

    if regexStrong.match(passwordAttempt) != None:#Strong
        print("Strong")
    elif regexWeak.match(passwordAttempt) != None:#Weak
        print("weak")
    else:#Invalid
        print("invalid")
    #userDataDB.s
else:
    raise ValueError("WTF?!?!?!?")
