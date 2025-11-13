from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from . import views
from projectTracker import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index_view),
    path('user-dashboard', views.user_dashboard_view, name='user-dashboard'),
    path('Connexion', LoginView.as_view(template_name='Tracker/sign-in.html'), name='Connexion'),
    path('Register', views.register_view, name='Register'),
    path('Deconnexion', views.deconnexion_view, name='Deconnexion'),

    path('Tracker/', include("Trackerapp.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)