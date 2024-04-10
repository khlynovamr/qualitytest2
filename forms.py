from django import forms
from django.contrib.auth import authenticate

from quality_tests_app.models import User


class AuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин'}), max_length=30,
                               required=True, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}), max_length=30,
                               required=True, label='Пароль', )

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Такого пользователя не существует!')
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль!')
            if not user.is_active:
                raise forms.ValidationError('Пользователь неактивен!')
        return super(AuthForm, self).clean(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

