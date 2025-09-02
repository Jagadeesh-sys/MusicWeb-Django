from django.contrib import admin
from django.urls import path
from music import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'), 
    path('base/', views.base, name='base'),
    path('all_songs/', views.all_songs, name='all_songs'),
    path('telugu_songs/', views.telugu_songs, name='telugu_songs'),
    path('hindi_songs/', views.hindi_songs, name='hindi_songs'),
    path('tamil_songs/', views.tamil_songs, name='tamil_songs'),
    path('english_songs/', views.english_songs, name='english_songs'),
    path('artists/', views.artists, name='artists'),
    path('artist/<str:singer_name>/', views.singer_detail, name='singer_detail'),
    path('new_songs/', views.new_songs, name='new_songs'),
    path('old_songs/', views.old_songs, name='old_songs'),
    path('trending_songs/', views.trending_songs, name='trending_songs'),
    path('list_songs/', views.list_songs, name='list_songs'),
    path('search/', views.search_view, name='search'),
    path('toggle_like/', views.toggle_like, name='toggle_like'),
    path('check_liked/', views.check_liked, name='check_liked'),
    path('liked_songs/', views.liked_songs, name='liked_songs'),
    path('profile/', views.user_profile, name='user_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
