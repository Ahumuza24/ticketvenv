from django import forms

from .models import Issue

class CreateIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'priority', 'attached_file']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'attached_file': forms.FileInput(attrs={'class': 'form-control'}),}


class UpdateIssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['title', 'description', 'category', 'priority', 'attached_file']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'attached_file': forms.FileInput(attrs={'class': 'form-control'}),}

