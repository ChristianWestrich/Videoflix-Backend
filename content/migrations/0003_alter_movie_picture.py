# Generated by Django 5.0.6 on 2024-06-26 06:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0002_remove_movie_thumbnail_movie_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="picture",
            field=models.ImageField(blank=True, null=True, upload_to="thumbnails"),
        ),
    ]
