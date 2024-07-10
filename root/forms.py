from django import forms
from .models import *


class ExcelDataForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        fields = ['excel_file']
        widgets = {
            'excel_file': forms.FileInput(attrs={'class': 'form-control-file', 'accept': '.xlsx, .xls'})
        }


class MockTestSolutionForm(forms.ModelForm):
    class Meta:
        model = MockTestSolution
        fields = ['mock_test_number', 'solution_file']
        widgets = {
            'mock_test_number': forms.TextInput(attrs={'class': 'form-control custom-class-for-input'}),
            'solution_file': forms.FileInput(attrs={'class': 'form-control-file custom-class-for-file-input'}),
        }
        labels = {
            'mock_test_number': 'Mock Test Number ',
            'solution_file': 'Solution File ',
        }


class StudyPlanForm(forms.ModelForm):
    class Meta:
        model = StudyPlan
        fields = ['name', 'pdf_file']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter plan name'
            }),
            'pdf_file': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),
        }


class CurrentAffair(forms.ModelForm):
    class Meta:
        model = CurrentAffairs
        fields = ['title', 'link', 'text', 'image']
