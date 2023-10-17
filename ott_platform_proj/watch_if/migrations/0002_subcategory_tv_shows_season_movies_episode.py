# Generated by Django 4.2.5 on 2023-10-05 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('watch_if', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watch_if.category')),
            ],
        ),
        migrations.CreateModel(
            name='Tv_shows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('language', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='content/images/')),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watch_if.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_number', models.PositiveIntegerField()),
                ('tv_show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watch_if.tv_shows')),
            ],
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('duration', models.PositiveIntegerField()),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='content/images/')),
                ('video_url', models.URLField(blank=True, max_length=255)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watch_if.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('duration', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('episode_number', models.PositiveIntegerField()),
                ('video_url', models.URLField(blank=True, max_length=255)),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watch_if.season')),
            ],
        ),
    ]
