# MusicApp (Django)

A simple music web application built with Django. Users can browse songs by language, view artists, like/unlike songs, search, and manage their profile. The project uses a custom user model and stores song files and images in the `media/` directory.

## Features
- **Custom user model** using `music.CustomUser` with mobile number and liked songs
- **Signup/Login** with username-password, plus **OTP flow (console demo)**
- **Browse songs** by language (Telugu, Hindi, Tamil, English)
- **Artists pages** inferred from images in `media/album_images/`
- **Like/Unlike songs** and view your liked songs
- **Search** songs by title or singer
- **Media uploads** for songs and images using `FileField`/`ImageField`

## Tech Stack
- **Backend:** Django 5
- **Database:** SQLite (default)
- **Static/Media:** Local filesystem (development)

## Requirements
Defined in `requirements.txt`:
- Django==5.0.2
- Pillow==10.3.0
- pydub==0.25.1
- pytube==15.0.0

Optional (for production or extra tooling):
- whitenoise (serve static files in production)
- django-environ (read settings from .env)
- gunicorn (Linux WSGI server)
- psycopg2-binary (PostgreSQL client)

Note: `pydub` may require `ffmpeg` installed on your system.

## Project Structure
Key paths (relative to repository root):
- `manage.py`
- `MusicApp/` – Django project settings (`settings.py`, `urls.py`, etc.)
- `music/` – App with models, views, urls, templates
- `media/` – Uploaded media files (album images, song images, songs)
- `templates/` – HTML templates (if present at project root)
- `static/` – Static assets (if present at project root)
- `requirements.txt`

## Local Setup
1. **Clone** the repository
2. **Create and activate a virtual environment**
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
7. Open http://127.0.0.1:8000 in your browser.

## Environment Variables
In development, default settings are used with `DEBUG=True`. For production you should configure:
- `SECRET_KEY` – a strong, unique value
- `DEBUG` – set to `False`
- `ALLOWED_HOSTS` – e.g. `yourdomain.com,localhost`

If you adopt `django-environ`, create a `.env` file and load these in `settings.py`.

## Media and Static Files
- **Media**
  - `MEDIA_URL = '/media/'`
  - `MEDIA_ROOT = BASE_DIR / 'media'`
  - Uploads go under `media/` (e.g., `album_images/`, `song_images/`, `songs/`). Ensure the directories exist or are created by Django on first upload.
- **Static**
  - `STATIC_URL = '/static/'`
  - In development, Django serves from `static/` directories defined in `STATICFILES_DIRS`.
  - For production, consider using WhiteNoise or a CDN and run `python manage.py collectstatic`.

## OTP Flow (Demo)
The OTP feature is a demo only: OTP codes are generated and printed to the console instead of being sent via SMS. To integrate with a real SMS provider, wire up `send_otp()` in `music/views.py` with a service like Twilio or AWS SNS.

## Notes on `pydub` and `ffmpeg`
If you plan to process audio files with `pydub`, install `ffmpeg`:
- Windows: install from https://www.gyan.dev/ffmpeg/builds/ and add `ffmpeg\bin` to PATH
- Verify: `ffmpeg -version`

## Deployment (Render example)
Typical steps for deploying on Render:
1. Ensure `requirements.txt` is at the repository root and includes all dependencies.
2. Create a new Web Service on Render pointing to this repo.
3. Environment
   - `PYTHON_VERSION` (e.g., `3.10`)
   - `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS=<your Render URL>`
4. Build Command
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```
5. Start Command (example)
   ```bash
   gunicorn MusicApp.wsgi:application --bind 0.0.0.0:$PORT
   ```
6. If using WhiteNoise, add it to `MIDDLEWARE` and set `STATIC_ROOT`, then run `collectstatic`.

## Troubleshooting
- If you see `ModuleNotFoundError`, ensure your virtualenv is activated and dependencies installed.
- If images or songs do not display, verify `MEDIA_ROOT`/`MEDIA_URL` configuration and that files exist under `media/`.
- On Windows, if `pydub` fails, confirm `ffmpeg` is installed and on PATH.

## License
This project is provided as-is; add your preferred license here (MIT, Apache 2.0, etc.).
