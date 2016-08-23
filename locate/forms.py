from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import re


class detailsForm(forms.Form):
    name=forms.CharField(max_length=100)
    phoneNumber=forms.CharField(max_length=100)


    def clean(self):
        data=self.cleaned_data['phoneNumber']
        data_arr=data.split(",")
        print "came in validation"
        for i in data_arr:
            if(re.match(r'^\+91[0-9]+$',i)):
                if(len(i)!=13):
                    errorText=i+" this number entered is less than 10 digits"
                    raise forms.ValidationError(errorText)
            else:
                x=re.match(r'^[0-9]+$',i)
                if not x:
                    errorText=i+" this number entered is not in proper format"
                    raise forms.ValidationError(errorText)
                elif len(i)!=10:
                    errorText=i+" this number entered is less than 10 digits"
                    raise forms.ValidationError(errorText)

        return data

class RegistrationForm(forms.Form):

    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
