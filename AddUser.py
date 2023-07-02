# -*- coding: utf-8 -*-
import pymongo


def main(email, name, date):
    client = pymongo.MongoClient(
        "mongodb+srv://ayushganna67:U9qpqS1V3tKy0sq1@deardiary.dn8lmbn.mongodb.net/")
    mydb = client["DearDiary"]
    usersCol = mydb["users"]
    if usersCol.find({"created_at": date}):
        usersCol.delete_one(
            {"email": email})
    mydict = {
        "email": email,
        "name": name,
        "created_at": date,
    }
    usersCol.insert_one(mydict)
