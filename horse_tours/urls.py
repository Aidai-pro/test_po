from django.urls import path
from . import views

app_name = 'horse_tours'

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('booking/', views.create_booking, name='create_booking'),
    path('comment/', views.add_comment, name='add_comment'),
    path('download-report/', views.download_report, name='download_report'),
]