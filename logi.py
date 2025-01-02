# This file contains most of the logic of the Esports Cyber App

import sqlite3, os, re, secrets, hashlib

CONST_PEPPER = "a160e1259fb5bdbdc7ef315fd78ad840"
CONST_DB_FILE = "Esports Cyber App DataBase.db"
UserDataDB = sqlite3.connect(CONST_DB_FILE)
UserDataDB.autocommit = True
DBCur = UserDataDB.cursor()

regexStrong = re.compile(r"(?=.{13,})(?=(.*[a-z]){2,})(?=(.*[A-Z]){2,})(?=(.*\d){2,})(?=(.*[^\w\d\s@#]){2,}).*$", re.MULTILINE | re.UNICODE)
regexWeak = re.compile(r"(?=.{8,})(?=(.*[a-z]){1,})(?=(.*[A-Z]){1,})(?=(.*\d){1,})(?=(.*[^\w\d\s@#]){1,}).*$", re.MULTILINE | re.UNICODE)

def DBCheck() -> None:
    # Make file
    if os.path.isfile(CONST_DB_FILE) and os.access(CONST_DB_FILE, os.R_OK):
        ...
    else:
        open(CONST_DB_FILE,"w").close()

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

def Login(UNOwen: str,PWOwen: str) -> int:
    if CheckForUser(UNOwen):
        salt = DBCur.execute("SELECT salt FROM userdata WHERE unowen = ?",(UNOwen,)).fetchone()[0]
        PWOwenCrypt = hashlib.sha3_512(bytes(str(PWOwen+CONST_PEPPER+salt), encoding='utf-8'),usedforsecurity=True).hexdigest()
        if PWOwenCrypt == DBCur.execute("SELECT hash FROM userdata WHERE unowen = ?",(UNOwen,)).fetchone()[0]:
            return 0 # Password is right
        else: return 411 # Password is wrong
    else: return 404 # No account

def Signup(UNOwen: str,PWOwen: str) -> int:
    if CheckForUser(UNOwen):
        return 409 # User already exists
    else:
        if regexWeak.match(PWOwen) != None: # Weak
            salt = secrets.token_hex(16)
            PWOwenCrypt = hashlib.sha3_512(bytes(str(PWOwen+CONST_PEPPER+salt), encoding='utf-8'),usedforsecurity=True).hexdigest()
            DBCur.execute("INSERT INTO userdata(unowen, hash, salt) VALUES(?,?,?);",(UNOwen,PWOwenCrypt,salt))

            if regexStrong.match(PWOwen) != None:return 0 # Strong    
            else:return 1 # Weak Password

        else:return 411 # Invalid PW

#Login("alfie", "AlfieLovesBacon123!\"")