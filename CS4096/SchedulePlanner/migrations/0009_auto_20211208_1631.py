# Generated by Django 3.2.7 on 2021-12-08 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SchedulePlanner', '0008_alter_courselog_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavedCourseLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SchedulePlanner.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='saved_courses',
            field=models.ManyToManyField(related_name='saved_courses', through='SchedulePlanner.SavedCourseLog', to='SchedulePlanner.Course'),
        ),
    ]