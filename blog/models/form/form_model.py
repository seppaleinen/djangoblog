from django import forms


class Form(forms.Form):
    select = forms.ChoiceField(choices=())

    def __init__(self, branches, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        self.fields['select'] = forms.ChoiceField(choices = branches)
