from .models import AddVacancy
from django import forms


class AddVacancyForm(forms.ModelForm):
    class Meta:
        model = AddVacancy
        fields = "__all__"