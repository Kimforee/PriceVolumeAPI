from django.urls import path
from .views import index, fetch_data, create_data_entry, update_data_entry, delete_data_entry, edit_data, delete_data

urlpatterns = [
    path('', index, name='index'),
    path('fetch-data/', fetch_data, name='fetch_data'),
    path('create-data-entry/', create_data_entry, name='create_data_entry'),
    path('update-data-entry/<str:entry_id>/', update_data_entry, name='update_data_entry'),
    path('delete-data-entry/<str:entry_id>/', delete_data_entry, name='delete_data_entry'),
    path('edit-data/<str:document_id>/', edit_data, name='edit_data'),

    path('delete-data/<str:document_id>/', delete_data, name='delete_data'),
]
