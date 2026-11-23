from django.urls import path
from . import views

app_name = 'horse_tours'

urlpatterns = [
    path('', views.tour_list, name='tour_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('booking/', views.create_booking, name='create_booking'),
    path('comment/', views.add_comment, name='add_comment'),
    path('download-report/', views.download_report, name='download_report'),
]