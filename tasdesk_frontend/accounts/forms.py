from django import forms
from .models import User, User_Details
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Kullanıcı Adı")
    password = forms.CharField(max_length=100, label="Parola", widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Kullanıcı adı ya da parolayı yanlış girdiniz')
            return super(LoginForm, self).clean()

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'is_designer'
        ]

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor")
        return password_confirm


class UserDetailAboutForm(forms.ModelForm):

    class Meta:
        model = User_Details
        fields = [
            'about',
        ]

class UserDetailExperiencesForm(forms.ModelForm):

    class Meta:
        model = User_Details
        fields = [
            'experiences',
        ]

class UserDetailEducationForm(forms.ModelForm):

    class Meta:
        model = User_Details
        fields = [
            'graduations',
        ]

class UserDetailLocationForm(forms.ModelForm):

    class Meta:
        model = User_Details
        fields = [
            'location',
        ]

class UserDetailSkillsForm(forms.ModelForm):

    class Meta:
        model = User_Details
        fields = [
            'skills',
        ]

class ChangeUserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = User_Details
        fields = [
            'user_profile_image'
        ]