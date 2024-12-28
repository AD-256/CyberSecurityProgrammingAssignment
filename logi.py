# This file contains most of the logic of the Esports Cyber App

import sqlite3, os, re, secrets, hashlib

CONST_PEPPER = "a160e1259fb5bdbdc7ef315fd78ad840"
DBFile = "2024-25_USW_Cyber_Esports_App.db"
UserDataDB = sqlite3.connect(DBFile)
UserDataDB.autocommit = True
DBCur = UserDataDB.cursor()

regexStrong = re.compile(r"(?=.{13,})(?=(.*[a-z]){2,})(?=(.*[A-Z]){2,})(?=(.*\d){2,})(?=(.*[^\w\d\s@#]){2,}).*$", re.MULTILINE | re.UNICODE)
regexWeak = re.compile(r"(?=.{8,})(?=(.*[a-z]){1,})(?=(.*[A-Z]){1,})(?=(.*\d){1,})(?=(.*[^\w\d\s@#]){1,}).*$", re.MULTILINE | re.UNICODE)

def DBCheck() -> None:
    # Make file
    if os.path.isfile(DBFile) and os.access(DBFile, os.R_OK):
        ...
    else:
        open(DBFile,"w").close()

    # Make DB
    TableMaker = """
    CREATE TABLE IF NOT EXISTS userdata (
    pk INTEGER PRIMARY KEY,
    unowen TEXT NOT NULL,
    hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    mfa TEXT
    );"""
    DBCur.execute(TableMaker)

def CheckForUser(User: str) -> bool:
    sql = """
    SELECT *
    FROM userdata
    WHERE unowen = ?
    ;"""
    return DBCur.execute(sql, (User,)).fetchone() != None
    ...

def Login(UNOwen: str,PWOwen: str) -> int:
    if CheckForUser(UNOwen):
        salt = DBCur.execute("")
        PWOwenCrypt = hashlib.sha3_512(bytes(str(PWOwen+CONST_PEPPER+salt), encoding='utf-8'),usedforsecurity=True).hexdigest()
        ...
    else:
        #error
        return 404
        ...

    ...

def Signup(UNOwen: str,PWOwen: str) -> int:
    
    if CheckForUser(UNOwen):
        return 409 # error
    else:
        if regexWeak.match(PWOwen) != None: # Weak
            salt = secrets.token_hex(16)
            PWOwenCrypt = hashlib.sha3_512(bytes(str(PWOwen+CONST_PEPPER+salt), encoding='utf-8'),usedforsecurity=True).hexdigest()
            DBCur.execute("INSERT INTO userdata(unowen, hash, salt) VALUES(?,?,?);",(UNOwen,PWOwenCrypt,salt))

            if regexStrong.match(PWOwen) != None:return 0 # Strong    
            else:return 1 # Weak Password

        else:return 411 # Invalid PW
