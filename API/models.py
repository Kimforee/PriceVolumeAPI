# api/models.py
import pymongo
from django.db import models  # This is not used, but we keep it for Django's sake

client = pymongo.MongoClient("mongodb+srv://keshavimperial:1A2V3hLjgmJ5blpv@clustera.y16gzea.mongodb.net/")
database = client["test_db"]
collection = database["user"]

class DataEntry:
    @classmethod
    def save(cls, price, volume):
        try:
            collection.insert_one({
                'priceNative': price,
                'volume': volume
            })
        except Exception as e:
            print(f"An error occurred while saving data: {e}")

    @classmethod
    def fetch_all(cls):
        try:
            return list(collection.find())
        except Exception as e:
            print(f"An error occurred while fetching data: {e}")
            return []

    @classmethod
    def update(cls, new_price, new_volume):
        try:
            collection.update_many(
                {},
                {'$set': {'priceNative': new_price, 'volume': new_volume}}
            )
        except Exception as e:
            print(f"An error occurred while updating data: {e}")

    @classmethod
    def delete_all(cls):
        try:
            collection.delete_many({})
        except Exception as e:
            print(f"An error occurred while deleting data: {e}")
