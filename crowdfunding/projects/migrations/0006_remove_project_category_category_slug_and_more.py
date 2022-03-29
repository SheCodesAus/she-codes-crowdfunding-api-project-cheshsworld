# Generated by Django 4.0.2 on 2022-03-26 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_category_project_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='none'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]