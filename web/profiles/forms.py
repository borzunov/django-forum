from django import forms
from captcha.fields import ReCaptchaField


class SignupForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=10)
    email = forms.EmailField(label='E-mail',
                             help_text='Вы сможете войти в аккаунт только после того, ' +
                                       'как перейдёте по ссылке из письма, которое придёт вам на почту')
    password = forms.CharField(label='Пароль', min_length=6, max_length=30, widget=forms.PasswordInput,
                               help_text='От 6 до 30 символов')
    confirm_password = forms.CharField(label='Повторите пароль', max_length=30, widget=forms.PasswordInput)

    captcha = ReCaptchaField()
    accept_agreement = forms.BooleanField(label='Обязуюсь соблюдать на форуме законы РФ', required=True)

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data['confirm_password']
