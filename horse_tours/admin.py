from django.contrib import admin
from .models import Category, Tour, Booking, Comment

admin.site.register(Category)
admin.site.register(Tour)
admin.site.register(Booking)
admin.site.register(Comment)