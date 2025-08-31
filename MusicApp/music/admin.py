from django.contrib import admin
from .models import Album, Songs
from .models import CustomUser

admin.site.register(Album)
admin.site.register(Songs)
admin.site.register(CustomUser)
