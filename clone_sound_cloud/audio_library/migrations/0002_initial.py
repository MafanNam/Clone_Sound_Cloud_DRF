# Generated by Django 4.2.7 on 2023-12-21 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("audio_library", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="track",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="user_of_likes",
            field=models.ManyToManyField(
                blank=True, related_name="likes_of_tracks", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="tracks",
            field=models.ManyToManyField(
                related_name="playlist_tracks", to="audio_library.track"
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="playlists",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="playedusertrack",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="played_track",
                to="audio_library.track",
            ),
        ),
        migrations.AddField(
            model_name="playedusertrack",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_played_track",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="license",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="licenses",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="track_comments",
                to="audio_library.track",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="album",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
