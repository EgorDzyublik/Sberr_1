# from .models import Input
# from django.forms import ModelForm, FileInput
#
# class InputForm(ModelForm):
#     class Meta:
#         model = Input
#         fields = ['texts']
#
#         widgets = {
#             'texts': FileInput(attrs={
#                 'class': 'addfile'
#             })
#         }

from django import forms

class InputForm(forms.Form):
    docfile = forms.FileField()