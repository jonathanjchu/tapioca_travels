# Generated by Django 2.2.1 on 2019-05-30 16:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190530_1225'),
        ('travels', '0002_auto_20190530_0304'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('picture_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='picture', to='travels.Location')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_loc_images', to='users.User')),
            ],
        ),
    ]