from django.contrib import admin
from django.urls import path
from myapp import views
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),
    path('',views.homepage,name='homepage'),
    path('signup/',views.signup, name='signup'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
]
=======
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('box_office/',views.box_office,name='box_office'),
    path('dashboard/',views.dashboard,name='dashboard'),

    path('',views.homepage,name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.SignupPage.as_view(), name='signup'),
]







# Ajoutez cette ligne pour servir les fichiers médias en développement.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 5c56ef9437575d9a6390df50010d7c400244dae7
