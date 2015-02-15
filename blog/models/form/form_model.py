from django import forms


class Form(forms.Form):
    OPTIONS = (('master', 'master'),('remote', 'remote'))
    select = forms.ChoiceField(choices=OPTIONS)