from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'adverts'

urlpatterns = [
    path(r'index/', advert_index, name="index"),
    path(r'create/', advert_create, name="create"),
    #path(r'<str:slug>/', advert_detail, name="detail"),
    path(r'<str:slug>/update', advert_update, name="update"),
    path(r'<str:slug>/delete', advert_delete, name="delete"),
    path(r'like/', advert_like, name="like"),
    path(r'createComment/', advert_comment_create, name="createComment")
]
