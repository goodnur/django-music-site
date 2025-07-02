from django import forms
from django.contrib.auth.models import User

class SimpleRegisterForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        username = cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Имя уже занято.")

        if password != password2:
            raise forms.ValidationError("Пароли не совпадают.")

        if password and len(password) < 9:
            raise forms.ValidationError("Пароль должен быть не короче 9 символов.")