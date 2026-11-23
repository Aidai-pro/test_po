from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Booking, Comment


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['tour', 'booking_date']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['tour', 'text']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Email',
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password_confirm")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data


class LoginWithCaptchaForm(AuthenticationForm):
    captcha = forms.CharField(
        label="Капча (введите ответ)",
        widget=forms.TextInput(attrs={'placeholder': 'Введите ответ с примера'})
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.request = request

    def clean_captcha(self):
        user_answer = self.cleaned_data.get('captcha', '').strip()
        expected_answer = str(self.request.session.get('captcha_answer', '')) if self.request else ''
        if not expected_answer or user_answer != expected_answer:
            raise forms.ValidationError("Неверный ответ капчи! Попробуйте снова.")
        return user_answer