from django import forms
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