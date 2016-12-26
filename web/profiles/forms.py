from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=10)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(label='Пароль', min_length=6, max_length=30, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Повторите пароль', max_length=30, widget=forms.PasswordInput)
    accept_agreement = forms.BooleanField(label='Обязуюсь соблюдать на форуме законы РФ', required=True)

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data['confirm_password']
