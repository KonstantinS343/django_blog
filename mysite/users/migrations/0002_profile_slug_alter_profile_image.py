# Generated by Django 4.1.5 on 2023-02-08 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.SlugField(max_length=255, null=True, unique=True, verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics/%Y/%m/%d'),
        ),
    ]
