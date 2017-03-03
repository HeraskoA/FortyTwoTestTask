from django import forms
from apps.hello.models import UserData
from apps.hello.widgets import DatePicker


class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={
                'cols': 35,
                'rows': 7}),
            'other_contacts': forms.Textarea(attrs={
                'cols': 35,
                'rows': 7}),
            'date_of_birth': DatePicker(),
            'photo': forms.FileInput(attrs={'id': 'id_photo'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field not in 'date_of_birth':
                self.fields[field].widget.attrs['class'] = 'form-control'
