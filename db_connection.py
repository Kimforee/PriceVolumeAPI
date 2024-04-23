import pymongo

client = pymongo.MongoClient("mongodb+srv://keshavimperial:1A2V3hLjgmJ5blpv@clustera.y16gzea.mongodb.net/")
database = client["test_db"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
        'NAME': 'MongoDB', 
    }
}
