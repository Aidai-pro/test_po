from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('', include('horse_tours.urls', namespace='horse_tours')),  # Теперь конные туры будут на главной!
    path('articles/', include('articles.urls')),
    path('blog/', include('blog.urls')),  # Старый блог переместили на /blog/
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)