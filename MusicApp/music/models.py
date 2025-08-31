from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Add additional fields if needed
    name = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True)
    liked_songs = models.ManyToManyField('Songs', related_name='liked_by', blank=True)


class OTP(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.mobile} - {self.otp}"
    
    def is_expired(self):
        # OTP expires after 10 minutes
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at < timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.username


class Album(models.Model):
    name = models.CharField(max_length=100, default='Default Album Name')
    image = models.ImageField(upload_to='album_images', blank=True, null=True)  # Album cover

    def __str__(self):
        return self.name


class Songs(models.Model):
    Language_Choice = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Telugu', 'Telugu'),
        ('Tamil', 'Tamil'),
    )

    title = models.CharField(max_length=100, default='Untitled')  
    album_name = models.ForeignKey('Album', related_name='songs', on_delete=models.CASCADE)
    song = models.FileField(upload_to='songs')
    image = models.FileField(upload_to='song_images', blank=True, null=True)  # song image (optional)
    singer = models.CharField(max_length=200)
    language = models.CharField(max_length=20, choices=Language_Choice, default='Telugu')

    def __str__(self):
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
