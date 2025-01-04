# This file contains most of the logic of the Esports Cyber App

import sqlite3, os, re, secrets, hashlib, pyotp, time

#Constants & Variables
CONST_PEPPER = "a160e1259fb5bdbdc7ef315fd78ad840"
CONST_DB_FILE = "Esports Cyber App DataBase.db"
UserDataDB = sqlite3.connect(CONST_DB_FILE)
UserDataDB.autocommit = True
DBCur = UserDataDB.cursor()

regexStrong = re.compile(r"(?=.{13,})(?=(.*[a-z]){2,})(?=(.*[A-Z]){2,})(?=(.*\d){2,})(?=(.*[^\w\d\s@#]){2,}).*$", re.MULTILINE | re.UNICODE)
regexWeak = re.compile(r"(?=.{8,})(?=(.*[a-z]){1,})(?=(.*[A-Z]){1,})(?=(.*\d){1,})(?=(.*[^\w\d\s@#]){1,}).*$", re.MULTILINE | re.UNICODE)

#Checks
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

def CheckForMFA(User: str) -> bool:
    if CheckForUser(User):
        sql = """
        SELECT mfa
        FROM userdata
        WHERE unowen = ?
        ;"""
        return DBCur.execute(sql, (User,)).fetchone()[0]
    else: return None
# Login & register
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

#MFA
def EnableMFA(User: str) -> str:
    if DBCur.execute("SELECT mfa FROM userdata WHERE unowen = ?;",(User,)).fetchone()[0] == None:
        DBCur.execute("UPDATE userdata SET mfa = ? WHERE unowen = ?",(pyotp.random_base32(),User))
        ...

def DisableMFA(User: str) -> None:
    if DBCur.execute("SELECT mfa FROM userdata WHERE unowen = ?;",(User,)).fetchone()[0] != None:
        DBCur.execute("UPDATE userdata SET mfa = ? WHERE unowen = ?",(None,User))
        ...

def MFALogin(User: str,Password: str,MFAToken: str) -> None:
    if Login(User,Password) == 0:
        MFAToken = re.sub(r"\D","",MFAToken)
        totp = pyotp.TOTP(CheckForMFA(User))
        totp.now()
        return totp.verify(MFAToken)
    else:print("Wtf?!?!")

#Login("alfie", "AlfieLovesBacon123!\"")
#print(CheckForMFA("alfie"))
#EnableMFA("alfie")
#print(DBCur.execute("SELECT mfa FROM userdata WHERE unowen = ?;",("alfie",)).fetchone()[0])
#DisableMFA("alfie")
#print(MFALogin("alfie","AlfieLovesBacon123!\"",input()))