from os import getenv

import pymongo

if not getenv("MONGO_URI"):
    raise EnvironmentError(f"Отсутвует переменная среды MONGO_URI")
MONGO_URI = getenv("MONGO_URI")
DB_NAME = getenv("DB_NAME")

myclient = pymongo.MongoClient("mongodb://admin:admin@172.17.0.1:27017")
mydb = myclient[DB_NAME]

users_col = mydb["users"]
