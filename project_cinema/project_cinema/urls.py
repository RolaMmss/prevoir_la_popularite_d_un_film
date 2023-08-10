from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('box_office/',views.box_office,name='box_office'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('start-scraping/', views.start_scraping, name='start-scraping'),


    path('',views.homepage,name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.SignupPage.as_view(), name='signup'),
]







# Ajoutez cette ligne pour servir les fichiers médias en développement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
