# This file contains most of the logic of the Esports Cyber App

import sqlite3
import os

DBFile = "2024-25_USW_Cyber_Esports_App.db"
UserDataDB = sqlite3.connect(DBFile)
UserDataDB.autocommit = True
DBCur = UserDataDB.cursor()

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
    pwowen TEXT NOT NULL,
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
        #error
        return 403
        ...
    else:
        
        ...

    ...

def Signup(UNOwen: str,PWOwen: str) -> int:
    if CheckForUser(UNOwen):
        #error
        return 403
        ...
    else:
        # start making account
        DBCur.execute("INSERT INTO userdata(unowen, pwowen) VALUES(?,?);",(UNOwen,PWOwen))
        ...
    ...
#DBCur.execute("INSERT INTO userdata(unowen, pwowen) VALUES(?,?)",("jack","test"))
Signup("jack","test")
print(CheckForUser("jack"))
DBCheck()