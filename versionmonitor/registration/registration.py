from django import forms
from registration.forms import RegistrationForm

__author__ = 'Semyon'


class RegistrationFormWithName(RegistrationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def save(self, commit=True):
        user = super(RegistrationFormWithName, self).save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user
