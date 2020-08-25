from django import forms
from .models import Advert, AdvertComment

class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = [
            'advert_title',
            'advert_content',
            'category',
            'advert_image',
            'is_public'
        ]
class CommentForm(forms.ModelForm):
    class Meta:
        model = AdvertComment
        fields = [
            'advert',
            'user',
            'comment_content',
        ]


