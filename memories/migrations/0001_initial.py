# Generated by Django 4.2.6 on 2023-12-03 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreateMemory',
            fields=[
                ('memory_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='uploads/')),
                ('user_id_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
