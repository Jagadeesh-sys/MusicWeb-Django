# Generated by Django 5.0.2 on 2024-03-29 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0002_remove_songs_album_delete_album'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Default Album Name', max_length=100)),
            ],
        ),
    ]
