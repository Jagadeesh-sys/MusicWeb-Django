from django.core.management.base import BaseCommand
from django.conf import settings
import os
from music.models import Album, Songs


class Command(BaseCommand):
    help = 'Set up albums from existing album images'

    def handle(self, *args, **options):
        album_images_dir = os.path.join(settings.MEDIA_ROOT, 'album_images')
        
        if not os.path.exists(album_images_dir):
            self.stdout.write(self.style.ERROR(f'Album images directory not found: {album_images_dir}'))
            return

        # Get all image files from album_images directory
        image_files = []
        for filename in os.listdir(album_images_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                image_files.append(filename)

        self.stdout.write(f'Found {len(image_files)} album images')

        # Create albums for each image
        for filename in image_files:
            # Extract album name from filename (remove extension and replace underscores)
            album_name = os.path.splitext(filename)[0].replace('_', ' ').title()
            
            # Check if album already exists
            album, created = Album.objects.get_or_create(
                name=album_name,
                defaults={'image': f'album_images/{filename}'}
            )
            
            if created:
                self.stdout.write(f'Created album: {album_name}')
            else:
                # Update existing album with image if it doesn't have one
                if not album.image:
                    album.image = f'album_images/{filename}'
                    album.save()
                    self.stdout.write(f'Updated album: {album_name} with image')

        # Now associate songs with albums based on singer names
        songs = Songs.objects.all()
        for song in songs:
            if song.singer:
                # Try to find a matching album by singer name
                singer_name = song.singer.strip()
                for album in Album.objects.all():
                    album_name_lower = album.name.lower()
                    singer_name_lower = singer_name.lower()
                    
                    # Check if singer name is in album name or vice versa
                    if (singer_name_lower in album_name_lower or 
                        album_name_lower in singer_name_lower or
                        singer_name_lower.replace(' ', '') in album_name_lower.replace(' ', '') or
                        album_name_lower.replace(' ', '') in singer_name_lower.replace(' ', '')):
                        
                        song.album_name = album
                        song.save()
                        self.stdout.write(f'Associated song "{song.title}" with album "{album.name}"')
                        break

        self.stdout.write(self.style.SUCCESS('Album setup completed!'))






