from django.forms import ModelForm, Select, Textarea
from .models import *

selected_lesson = '-'


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['lesson', 'comment']
        widgets = {
            'lesson': Select(
                attrs={
                    'placeholder': selected_lesson,
                }
            ),
            'comment': Textarea(
                attrs={
                    'rows': '2',
                    'class': 'form-control',
                    'placeholder': 'Комментарии',
                }),
        }
