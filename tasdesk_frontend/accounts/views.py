from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404 ,reverse
from django.contrib.auth import authenticate, login, logout

from tasdesk_frontend.accounts.storage import OverwriteStorage
from tasdesk_frontend.home.views import home_view
from .forms import RegisterForm, LoginForm, UserDetailAboutForm, UserDetailExperiencesForm, UserDetailEducationForm, UserDetailLocationForm,UserDetailSkillsForm,ChangeUserProfilePictureForm
from .models import User, User_Details, User_Messages, User_Reviews


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home:home')
    return render(request, 'tasdesk-frontend/sign/signin.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            User_Details.objects.create(user_id=user.id)
            login(request, new_user)
            return redirect('home:home')
    else:
        return render(request, 'tasdesk-frontend/sign/signup.html')


def logout_view(request):
    logout(request)
    return redirect('home:home')


def designer_profile_view(request, username):
    username = get_object_or_404(User, username=username)
    return render(request, 'tasdesk-frontend/user-profile/user-profile.html',{ "username": username})


def edit_userdetail_about(request):

    detail = get_object_or_404(User_Details, user=request.user)
    form = UserDetailAboutForm(request.POST or None, request.FILES or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile',kwargs={'username': request.user}))

    return redirect(reverse('accounts:profile', kwargs={'username': request.user}))


def edit_userdetail_experiences(request):

    detail = get_object_or_404(User_Details, user=request.user)
    form = UserDetailExperiencesForm(request.POST or None, request.FILES or None, instance=detail)

    print(request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile',kwargs={'username': request.user}))

    return redirect(reverse('accounts:profile', kwargs={'username': request.user}))


def edit_userdetail_education(request):

    detail = get_object_or_404(User_Details, user=request.user)
    form = UserDetailEducationForm(request.POST or None, request.FILES or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile', kwargs={'username': request.user}))

    return redirect(reverse('accounts:profile', kwargs={'username': request.user}))


def edit_userdetail_location(request):

    detail = get_object_or_404(User_Details, user=request.user)
    form = UserDetailLocationForm(request.POST or None, request.FILES or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile',kwargs={'username': request.user}))

    return redirect(reverse('accounts:profile', kwargs={'username': request.user}))


def edit_userdetail_skills(request):

    detail = get_object_or_404(User_Details, user=request.user)
    form = UserDetailSkillsForm(request.POST or None, request.FILES or None, instance=detail)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('accounts:profile',kwargs={'username': request.user}))

    return redirect(reverse('accounts:profile', kwargs={'username': request.user}))


def change_profile_img(request):

    detail = get_object_or_404(User_Details, user=request.user)

    if request.method == 'POST':
        form = ChangeUserProfilePictureForm(request.POST, request.FILES, instance=detail)

        if form.is_valid():
            form.save()

            return redirect(reverse('accounts:profile', kwargs={'username': request.user}))

    return render(request,reverse('accounts:profile', kwargs={'username': request.user}))

