from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [

    path('login', login_view, name="login_view"),
    path('register', register_view, name="register_view"),
    path('logout', logout_view, name='logout'),
    path('profile/<str:username>/', designer_profile_view,name='profile'),
    path('update_about/', edit_userdetail_about, name = 'edit_about'),
    path('update_experiences/', edit_userdetail_experiences, name = 'edit_experiences'),
    path('update_education/', edit_userdetail_education, name = 'edit_education'),
    path('update_location/', edit_userdetail_location, name = 'edit_location'),
    path('update_skills/', edit_userdetail_skills,name = 'edit_skills'),
    path('change_user_profile_image/', change_profile_img, name = 'change_user_profile_image')

]
