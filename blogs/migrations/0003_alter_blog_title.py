# Generated by Django 4.2.6 on 2023-10-17 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_alter_blog_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
