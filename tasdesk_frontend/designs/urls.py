from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'designs'

urlpatterns = [
    path(r'index/', design_index, name="index"),
    path(r'create/', design_create, name="create"),
    #path(r'<str:slug>/', design_detail, name="detail"),
    path(r'<str:slug>/update', design_update, name="update"),
    path(r'<str:slug>/delete', design_delete, name="delete"),
    path(r'like/', design_like, name="like"),
    path(r'createComment/', design_comment_create, name="createComment")
]
