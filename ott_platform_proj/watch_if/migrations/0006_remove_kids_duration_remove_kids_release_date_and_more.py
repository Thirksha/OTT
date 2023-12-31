# Generated by Django 4.2.5 on 2023-10-07 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watch_if', '0005_kids_rating_movies_rating_tv_shows_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kids',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='kids',
            name='release_date',
        ),
        migrations.RemoveField(
            model_name='kids',
            name='video_url',
        ),
        migrations.AddField(
            model_name='kids',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='watch_if.category'),
        ),
        migrations.AddField(
            model_name='movies',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='watch_if.category'),
        ),
        migrations.AddField(
            model_name='tv_shows',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='watch_if.category'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='video_url',
            field=models.URLField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='movies',
            name='video_url',
            field=models.URLField(blank=True, max_length=255),
        ),
    ]
