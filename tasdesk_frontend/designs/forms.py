from django import forms
from .models import Design, DesignComment

class DesignForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = [
            'design_title',
            'design_content',
            'category',
            'design_image',
            'is_public'
        ]
class CommentForm(forms.ModelForm):
    class Meta:
        model = DesignComment
        fields = [
            'design',
            'user',
            'comment_content',
        ]


