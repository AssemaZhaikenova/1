from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_v, name='login'),
    path('lesson/', views.lesson, name='lesson'),
    path('mylessons/', views.mylesson, name='mylessons'),
    path('logout/', views.logout_view, name='logout'),
    path('requests/', views.requests, name='requests'),
    path('addrequest/', views.select_view, name='addrequest'),
    path('addrequest/<int:id>/', views.select_view, name='addrequest'),
    path('coach/', views.coach, name='coach'),
    path('disciplines/', views.disciplines, name='disciplines'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
