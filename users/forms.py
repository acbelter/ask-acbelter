from django.core.exceptions import ValidationError
from django.forms import forms, CharField, EmailField, ImageField
from users.models import Member


class RegistrationForm(forms.Form):
    login = CharField()
    email = EmailField()
    nick = CharField()
    password = CharField()
    repeat_password = CharField()
    avatar = ImageField(required=False)

    def clean_login(self):
        if len(self.cleaned_data['login']) > 32:
            raise ValidationError(u'Too long login.')
        if Member.objects.filter(username=self.cleaned_data['login']).exists():
            raise ValidationError(u'This login already exists.')
        return self.cleaned_data['login']

    def clean_email(self):
        if Member.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(u'This email already exists.')
        return self.cleaned_data['email']

    def clean_nick(self):
        if len(self.cleaned_data['nick']) > 32:
            raise ValidationError(u'Too long nick.')
        return self.cleaned_data['nick']

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

        if password and password != repeat_password:
            raise ValidationError("Passwords doesn't match.")

        return self.cleaned_data

