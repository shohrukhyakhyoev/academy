# Generated by Django 4.2.6 on 2023-11-10 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='url',
            field=models.CharField(default='https://www.youtube.com/@iut_AcademicHelp', max_length=150),
        ),
    ]