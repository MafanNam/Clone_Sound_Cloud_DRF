# Generated by Django 4.2.7 on 2023-12-01 23:02

import base.services
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oauth', '0002_alter_follower_user_alter_sociallink_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('private', models.BooleanField(default=False)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=base.services.get_path_upload_album, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), base.services.validate_size_image])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='oauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='oauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link_of_author', models.CharField(blank=True, max_length=500, null=True)),
                ('file', models.FileField(upload_to=base.services.get_path_upload_track, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wev']), base.services.validate_size_audio])),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('plays_count', models.PositiveIntegerField(default=0)),
                ('download', models.PositiveIntegerField(default=0)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='audio_library.album')),
                ('genre', models.ManyToManyField(related_name='track_genres', to='audio_library.genre')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='license_tracks', to='audio_library.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='oauth.userprofile')),
                ('user_of_likes', models.ManyToManyField(related_name='likes_of_tracks', to='oauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=base.services.get_path_upload_playlist, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), base.services.validate_size_image])),
                ('tracks', models.ManyToManyField(related_name='track_playlists', to='audio_library.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to='oauth.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_comments', to='audio_library.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='oauth.userprofile')),
            ],
        ),
    ]