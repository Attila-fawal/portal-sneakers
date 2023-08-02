from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'id': 'id_text'}))
    
    class Meta:
        model = Comment
        fields = ('text',)
