from django.contrib import admin
from django.urls import path, include
from myapp import views
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('box_office/',views.box_office,name='box_office'),
    path('dashboard/',views.dashboard,name='dashboard'),

    
    path('',views.homepage,name='homepage'),
    path('accounts/', include('django.contrib.auth.urls')),   
    path('signup/', views.SignupPage.as_view(), name='signup'),
]