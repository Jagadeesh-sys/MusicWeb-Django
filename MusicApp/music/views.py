
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Songs, Artist, OTP
from django.conf import settings
import os
import re
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from .models import CustomUser
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random


def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_otp(mobile):
    """Send OTP to mobile number (placeholder for actual SMS service)"""
    # In production, integrate with SMS service like Twilio, AWS SNS, etc.
    otp = generate_otp()
    
    # Save OTP to database
    OTP.objects.filter(mobile=mobile).delete()  # Remove old OTPs
    otp_obj = OTP.objects.create(mobile=mobile, otp=otp)
    
    # For development, print OTP to console
    print(f"OTP for {mobile}: {otp}")
    
    return otp_obj

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        
        # Check if mobile number already exists
        if CustomUser.objects.filter(mobile=mobile).exists():
            return JsonResponse({'success': False, 'message': 'Mobile number already registered.'})
        
        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already taken.'})
        
        if password == confirm_password:
            try:
                user = CustomUser.objects.create_user(username=username, password=password)
                user.name = name
                user.mobile = mobile
                user.save()
                return JsonResponse({'success': True, 'message': 'Account created successfully!'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': f'Error creating account: {str(e)}'})
        else:
            # Handle password mismatch error
            return JsonResponse({'success': False, 'message': 'Passwords do not match.'})
    
    # For GET requests, return the signup page
    return render(request, 'music/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # Authenticate using username (Django's default)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
        
    return render(request, 'music/login.html')

def send_otp_view(request):
    """Send OTP to mobile number"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        
        if not mobile:
            return JsonResponse({'success': False, 'message': 'Mobile number is required'})
        
        # Check if user exists
        try:
            user = CustomUser.objects.get(mobile=mobile)
            # Send OTP
            otp_obj = send_otp(mobile)
            return JsonResponse({
                'success': True, 
                'message': f'OTP sent to {mobile}. Check console for development.',
                'mobile': mobile
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Mobile number not registered. Please sign up first.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def verify_otp_view(request):
    """Verify OTP and login user"""
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        otp = request.POST.get('otp')
        
        if not mobile or not otp:
            return JsonResponse({'success': False, 'message': 'Mobile number and OTP are required'})
        
        try:
            # Get the latest OTP for this mobile
            otp_obj = OTP.objects.filter(mobile=mobile).order_by('-created_at').first()
            
            if not otp_obj:
                return JsonResponse({'success': False, 'message': 'No OTP found for this mobile number'})
            
            if otp_obj.is_expired():
                return JsonResponse({'success': False, 'message': 'OTP has expired. Please request a new one.'})
            
            if otp_obj.otp != otp:
                return JsonResponse({'success': False, 'message': 'Invalid OTP'})
            
            # OTP is valid, login user
            user = CustomUser.objects.get(mobile=mobile)
            auth_login(request, user)
            
            # Mark OTP as verified
            otp_obj.is_verified = True
            otp_obj.save()
            
            return JsonResponse({
                'success': True, 
                'message': 'Login successful!',
                'redirect_url': '/'
            })
            
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def logout_view(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def toggle_like(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            song_id = data.get('song_id')
            song = Songs.objects.get(id=song_id)
            
            if song in request.user.liked_songs.all():
                request.user.liked_songs.remove(song)
                is_liked = False
            else:
                request.user.liked_songs.add(song)
                is_liked = True
            
            return JsonResponse({
                'success': True,
                'is_liked': is_liked,
                'message': 'Song liked!' if is_liked else 'Song unliked!'
            })
        except Songs.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Song not found!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request!'
    })


@csrf_exempt
def check_liked(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            song_id = data.get('song_id')
            song = Songs.objects.get(id=song_id)
            
            is_liked = song in request.user.liked_songs.all()
            
            return JsonResponse({
                'success': True,
                'is_liked': is_liked
            })
        except Songs.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Song not found!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request!'
    })


def liked_songs(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    liked_songs_list = request.user.liked_songs.all()
    return render(request, 'music/liked_songs.html', {
        'liked_songs': liked_songs_list
    })


def home(request):
    username = request.user.name if request.user.is_authenticated else None

    telugu_songs = Songs.objects.filter(language='Telugu')
    hindi_songs = Songs.objects.filter(language='Hindi')
    tamil_songs = Songs.objects.filter(language='Tamil')
    english_songs = Songs.objects.filter(language='English')

    # Build top artists list with their images from album images
    top_artists = []
    try:
        # Create a mapping of image filenames to actual artist names
        image_to_artist_mapping = {
            'anirudh': 'Anirudh',
            'arjith_singh': 'Arjith Singh',
            'dsp': 'Devi Sri Prasad',
            'sid_sriram': 'Sidsriram',  # Fixed: database has 'Sidsriram' not 'Sid Sriram'
            'sachin-jigar': 'Sachin-Jigar',  # Added Sachin-Jigar
            'anurag_kulkarni': 'Anurag Kulakarni',  # Added Anurag Kulakarni (note spelling difference)
            'anand_aravindakshan': 'Anand Aravindakshan'
        }
        
        images_dir = os.path.join(settings.MEDIA_ROOT, 'album_images')
        if os.path.isdir(images_dir):
                # Preload candidates once
                candidates = Songs.objects.exclude(singer__isnull=True).exclude(singer__exact='')
                for filename in os.listdir(images_dir):
                    if len(top_artists) >= 6:  # Limit to 6 artists
                        break
                        
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        # Extract artist name from filename
                        name_part = os.path.splitext(filename)[0].lower()
                        
                        # Use mapping to get correct artist name
                        artist_name = image_to_artist_mapping.get(name_part, name_part.replace('_', ' ').title())
                        
                        # Find this artist's songs
                        artist_songs = [s for s in candidates if s.singer.lower() == artist_name.lower()]
                        
                        if artist_songs:  # Only add if artist has songs
                            # Construct the URL expected by the template
                            image_url = os.path.join(settings.MEDIA_URL, 'album_images', filename).replace('\\', '/')
                            artist_dict = {
                                'name': artist_name,
                                'image': {'url': image_url},
                                'songs': artist_songs
                            }
                            top_artists.append(artist_dict)
    except Exception as e:
        # If any error occurs, leave artists empty
        print(f"Error building top artists: {e}")
        pass

    # New, Trending, All, Old Songs sections
    all_songs = Songs.objects.all()
    new_songs = Songs.objects.order_by('-id')[:12]
    trending_songs = Songs.objects.order_by('?')[:12]
    old_songs = Songs.objects.order_by('id')[:12]

    context = {
        'telugu_songs': telugu_songs,
        'hindi_songs': hindi_songs,
        'tamil_songs': tamil_songs,
        'english_songs': english_songs,
        'top_artists': top_artists,  # Changed to 'top_artists'
        'new_songs': new_songs,
        'trending_songs': trending_songs,
        'all_songs': all_songs,
        'old_songs': old_songs,
        'username': username,
    }

    return render(request, 'music/home.html', context)






def base(request):
    return render(request, 'music/base.html')


def all_songs(request):
    songs = Songs.objects.all()
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        # Include all songs, with or without images
        if song.image:
            # Constructing the image URL for songs with images
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
        else:
            # For songs without images, use None or a default image
            songs_with_images.append((song, None))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images})


def telugu_songs(request):
    songs = Songs.objects.filter(language='Telugu')
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        if song.image:
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
        else:
            songs_with_images.append((song, None))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images, 'language': 'Telugu'})


def hindi_songs(request):
    songs = Songs.objects.filter(language='Hindi')
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        if song.image:
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
        else:
            songs_with_images.append((song, None))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images, 'language': 'Hindi'})


def tamil_songs(request):
    songs = Songs.objects.filter(language='Tamil')
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        if song.image:
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
        else:
            songs_with_images.append((song, None))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images, 'language': 'Tamil'})


def english_songs(request):
    songs = Songs.objects.filter(language='English')
    media_url = settings.MEDIA_URL
    songs_with_images = []
    for song in songs:
        if song.image:
            image_url = os.path.join(media_url, str(song.image))
            songs_with_images.append((song, image_url))
        else:
            songs_with_images.append((song, None))
    return render(request, 'music/all_songs.html', {'songs_with_images': songs_with_images, 'language': 'English'})


def artists(request):
    # Build artists list from album_images directory using the same logic as home view
    artists = []
    try:
        # Create a mapping of image filenames to actual artist names
        image_to_artist_mapping = {
            'anirudh': 'Anirudh',
            'arjith_singh': 'Arjith Singh',
            'dsp': 'Devi Sri Prasad',
            'sid_sriram': 'Sidsriram',  # Fixed: database has 'Sidsriram' not 'Sid Sriram'
            'sachin-jigar': 'Sachin-Jigar',  # Added Sachin-Jigar
            'anurag_kulkarni': 'Anurag Kulakarni',  # Added Anurag Kulakarni
            'anand_aravindakshan': 'Anand Aravindakshan'
        }
        
        images_dir = os.path.join(settings.MEDIA_ROOT, 'album_images')
        if os.path.isdir(images_dir):
                # Preload candidates once
                candidates = Songs.objects.exclude(singer__isnull=True).exclude(singer__exact='')
                for filename in os.listdir(images_dir):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        # Extract artist name from filename
                        name_part = os.path.splitext(filename)[0].lower()
                        
                        # Use mapping to get correct artist name
                        artist_name = image_to_artist_mapping.get(name_part, name_part.replace('_', ' ').title())
                        
                        # Find this artist's songs
                        artist_songs = [s for s in candidates if s.singer.lower() == artist_name.lower()]
                        
                        if artist_songs:  # Only add if artist has songs
                            # Construct the URL expected by the template
                            image_url = os.path.join(settings.MEDIA_URL, 'album_images', filename).replace('\\', '/')
                            artist_dict = {
                                'name': artist_name,
                                'image': {'url': image_url},
                                'songs': artist_songs
                            }
                            artists.append(artist_dict)
    except Exception as e:
        # If any error occurs, leave artists empty
        print(f"Error building artists: {e}")
        pass
    
    return render(request, 'music/artists.html', {'singers': artists})


def singer_detail(request, singer_name):
    # Normalize name to match how it's stored in Songs.singer
    normalized = singer_name.replace('-', ' ').replace('_', ' ').strip()
    target = re.sub(r'\s+', '', normalized).lower()
    candidates = Songs.objects.exclude(singer__isnull=True).exclude(singer__exact='')
    songs = [s for s in candidates if re.sub(r'\s+', '', s.singer or '').lower() == target]
    
    # Find artist image from album_images directory
    artist_image_url = None
    try:
        # Create a mapping of image filenames to actual artist names
        image_to_artist_mapping = {
            'anirudh': 'Anirudh',
            'arjith_singh': 'Arjith Singh',
            'dsp': 'Devi Sri Prasad',
            'sid_sriram': 'Sidsriram',
            'sachin-jigar': 'Sachin-Jigar',
            'anurag_kulkarni': 'Anurag Kulakarni',
            'anand_aravindakshan': 'Anand Aravindakshan'
        }
        
        images_dir = os.path.join(settings.MEDIA_ROOT, 'album_images')
        if os.path.isdir(images_dir):
                for filename in os.listdir(images_dir):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        name_part = os.path.splitext(filename)[0].lower()
                        artist_name = image_to_artist_mapping.get(name_part, name_part.replace('_', ' ').title())
                        
                        if artist_name.lower() == normalized.lower():
                            artist_image_url = os.path.join(settings.MEDIA_URL, 'album_images', filename).replace('\\', '/')
                            break
    except Exception:
        pass
    
    # Generate mock monthly listeners (you can replace this with real data later)
    import random
    monthly_listeners = f"{random.randint(1000000, 99999999):,}"
    
    return render(request, 'music/singer_detail.html', {
        'singer_name': normalized,
        'songs': songs,
        'artist_image_url': artist_image_url,
        'monthly_listeners': monthly_listeners,
    })


def new_songs(request):
    songs = Songs.objects.order_by('-id')[:48]
    return render(request, 'music/new_songs.html', {'songs': songs})


def old_songs(request):
    songs = Songs.objects.order_by('id')[:48]
    return render(request, 'music/old_songs.html', {'songs': songs})


def trending_songs(request):
    songs = Songs.objects.order_by('?')[:48]
    return render(request, 'music/trending_songs.html', {'songs': songs})


def display_songs(request):
    # Assuming the user's favorite songs are stored in a UserProfile model
    favorite_songs = request.user.profile.favorite_songs.all()
    return render(request, 'music/display_songs.html', {'favorite_songs': favorite_songs})


def list_songs(request):
    songs = Songs.objects.all()
    return render(request, 'music/list_songs.html', {'songs': songs})


def index(request):
    return render(request, 'music/index.html')


def search_view(request):
    query = request.GET.get('query', '').strip()
    results = []
    if query:
        results = Songs.objects.filter(Q(title__icontains=query) | Q(singer__icontains=query))
    return render(request, 'music/search.html', {'query': query, 'results': results})


def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Get user's liked songs
    liked_songs = request.user.liked_songs.all()
    
    # Get user's play count (you can implement this based on your needs)
    total_play_count = liked_songs.count() * 1000  # Placeholder
    
    # Get user's favorite artists (artists of liked songs)
    favorite_artists = set()
    for song in liked_songs:
        favorite_artists.add(song.singer)
    
    context = {
        'user': request.user,
        'liked_songs': liked_songs,
        'total_play_count': total_play_count,
        'favorite_artists': list(favorite_artists)[:5],  # Top 5 artists
        'monthly_listeners': f"{total_play_count:,}",
    }
    
    return render(request, 'music/user_profile.html', context)
