from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from .models import DataEntry
import pymongo
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.shortcuts import render
from django.shortcuts import render, redirect  # Add redirect import
import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.urls import reverse
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = pymongo.MongoClient("mongodb+srv://keshavimperial:1A2V3hLjgmJ5blpv@clustera.y16gzea.mongodb.net/")
db = client.test_db
collection = db["user"]  # Change "medicinedetails" to the actual collection name


def index(request):
    try:    
        data = list(collection.find_one({}))
        cursor = collection.find({})

        data = []
        for document in cursor:
            pair_data = {
                'volume_h24': document["pairs"][0]["volume"]["h24"],
                'price_native': document["pairs"][0]["priceNative"]
            }
            data.append(pair_data)
     
        return render(request, 'index.html', {'data': data})
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {e}")

@csrf_exempt
def fetch_data(request):
    try:
        cursor = collection.find({})
        data = []
        for document in cursor:
            # Convert ObjectId to string
            document['_id'] = str(document['_id'])
            
            data.append(document)
            print('hello')
            print(document['_id'])
        return render(request, 'fetched_data.html', {'data': data})
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {e}")

@csrf_exempt
def create_data_entry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            price = data.get('priceNative')
            volume = data.get('volume')
            if price is not None and volume is not None:
                # Create a new data entry
                new_entry = DataEntry(price=price, volume=volume)
                new_entry.save()
                return JsonResponse({'message': 'Data entry created successfully'}, status=201)
            else:
                return HttpResponseBadRequest('Missing required fields: priceNative, volume')
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")
    else:
        return HttpResponseBadRequest('Only POST requests are allowed')


@csrf_exempt
def update_data_entry(request, entry_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_price = data.get('priceNative')
            new_volume = data.get('volume')
            if new_price is not None or new_volume is not None:
                # Update data entry if new price or volume is provided
                DataEntry.update(entry_id, new_price, new_volume)
                return JsonResponse({'message': 'Data entry updated successfully'})
            else:
                return HttpResponseBadRequest('Missing fields: priceNative, volume')
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")
    else:
        return HttpResponseBadRequest('Only PUT requests are allowed')

@csrf_exempt
def delete_data_entry(request, entry_id):
    if request.method == 'DELETE':
        try:
            DataEntry.delete(entry_id)
            return JsonResponse({'message': 'Data entry deleted successfully'})
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")
    else:
        return HttpResponseBadRequest('Only DELETE requests are allowed')


# def edit_data(request, document_id):
#     try:
#         # Convert the document_id from string to ObjectId for MongoDB query
#         document_id = ObjectId(document_id)
#         document = collection.find_one({'_id': document_id})
#         if not document:
#             logger.error(f"Document with ID {document_id} not found")
#             return render(request, 'document_not_found.html', {'document_id': document_id})
        
#         if request.method == 'POST':
#             # Handle form submission to update the document
#             updated_data = {
#                 'pairs.$.volume.h24': request.POST.get('volume_h24'),
#                 'pairs.$.priceNative': request.POST.get('price_native')
#                 # Add other fields as needed
#             }
#             # Update the document in the MongoDB collection
#             # Note: This assumes you want to update the first pair in the pairs array. Adjust as necessary.
#             collection.update_one({'_id': document_id}, {"$set": updated_data})
#             # Retrieve the updated document
#             document = collection.find_one({'_id': document_id})
#             return render(request, 'edit_data.html', {'document': document})
#         else:
#             return render(request, 'edit_data.html', {'document': document})
#     except Exception as e:
#         logger.exception("An error occurred in edit_data view:")
#         return HttpResponseBadRequest(f"An error occurred: {e}")

def edit_data(request):
    print('hello')
    if request.method == 'POST':
        print('hello')
        document_id = request.POST.get('document_id')
        pair_address = request.POST.get('pair_address')
        new_price_native = request.POST.get('new_price_native')

        collection = MongoClient()['your_database']['your_collection']
        collection.update_one(
            {'_id': ObjectId(document_id)},
            {'$set': {'pairs.$[pair].priceNative': new_price_native}},
            array_filters=[{'pair.pairAddress': pair_address}]
        )

        return HttpResponseRedirect(reverse('fetch_data'))
    else:
        # Render your update form here
        pass



def delete_data(request, document_id):
    # Logic to delete the document by document_id
    try:
        collection.delete_one({'_id': document_id})
        return redirect('fetch_data')
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {e}")