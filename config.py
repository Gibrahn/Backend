import pymongo
import certifi

con_str="mongodb+srv://gibrahn:Hisoka69@cluster0.4oicb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())

db = client.get_database("OnlineStore")