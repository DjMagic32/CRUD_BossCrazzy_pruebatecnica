from django import forms
from ads.models import Songs
from django.forms import ModelForm

class CreateForm(ModelForm):
       class Meta:
        model = Songs
        fields = ['song', 'artista', 'category', 'content', 'urlvideo']