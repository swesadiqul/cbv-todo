from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ('title', 'status', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'status': forms.Select(attrs={'class': 'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
