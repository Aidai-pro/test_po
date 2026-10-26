from django.urls import path
from articles.views import (
    ArticleListView, ArticleDetailView, ArticleCreateView, 
    ArticleUpdateView, ArticleDeleteView, download_report
)

app_name = 'articles'

urlpatterns = [
    path('', ArticleListView.as_view(), name='list'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='detail'),
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ArticleUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', ArticleDeleteView.as_view(), name='delete'),
    path('export-report/', download_report, name='export_report'),
]