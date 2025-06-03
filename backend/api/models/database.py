from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017" 

client = MongoClient(MONGO_URL)
db = client["local"]  
products_collection = db.get_collection("products")