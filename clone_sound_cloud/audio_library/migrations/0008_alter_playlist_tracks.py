# Generated by Django 4.2.7 on 2023-12-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audio_library', '0007_alter_playedusertrack_played_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(related_name='playlist_tracks', to='audio_library.track'),
        ),
    ]