"""
URL configuration for Music_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Music import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('base/', views.base, name='base'),
    path('all_songs/',views.all_songs, name='all_songs'),
    path('new_songs/', views.new_songs, name='new_songs'),
    path('old_songs/', views.old_songs, name='old_songs'),
    path('trending_songs/', views.trending_songs, name='trending_songs'),
    path('search/', views.search_view, name='search'),
    path('artist/<int:artist_id>/songs/', views.artists, name='artists'),
    path('favorite-songs/', views.display_favorite_songs, name='display_favorite_songs'),






] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




