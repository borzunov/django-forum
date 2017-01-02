from django import forms
from captcha.fields import ReCaptchaField


class SignupForm(forms.Form):
    username = forms.CharField(max_length=10)
    email = forms.EmailField(help_text='You can log in only after following an activation link ' +
                                       'that will be sent to your email')
    password = forms.CharField(min_length=6, max_length=30, widget=forms.PasswordInput,
                               help_text='From 6 to 30 characters')
    confirm_password = forms.CharField(label='Repeat password', max_length=30, widget=forms.PasswordInput)

    captcha = ReCaptchaField()
    accept_agreement = forms.BooleanField(label='I agree to follow university rules on this forum', required=True)

    def clean_confirm_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Passwords don\'t match')
        return self.cleaned_data['confirm_password']
