# Generated by Django 3.2.12 on 2024-05-03 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0002_remove_test_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonprogress',
            name='progress',
        ),
        migrations.AddField(
            model_name='lessonprogress',
            name='is_lesson_done',
            field=models.BooleanField(default=False),
        ),
    ]
