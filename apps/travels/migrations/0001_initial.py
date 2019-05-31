# Generated by Django 2.2.1 on 2019-05-29 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accomodations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=32)),
                ('accomodation_type', models.IntegerField(choices=[(0, 'Private Home'), (1, 'Hotel'), (2, 'Hostel'), (3, 'Air BnB'), (4, 'Couchsurfing'), (5, 'Camping'), (6, 'Streets')])),
                ('price_per_night', models.FloatField()),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location_type', models.CharField(max_length=64)),
                ('info', models.TextField(max_length=1024)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('fees', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('added_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations_added', to='users.User')),
                ('parent_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_locations', to='travels.Location')),
            ],
        ),
        migrations.CreateModel(
            name='Transportation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.IntegerField(choices=[(0, 'Foot'), (1, 'Personal Car'), (2, 'Bus'), (3, 'Train'), (4, 'Airplane'), (5, 'Subway'), (6, 'Cab')])),
                ('company_name', models.CharField(max_length=32)),
                ('price', models.FloatField()),
                ('origin', models.CharField(max_length=64)),
                ('destination', models.CharField(max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_private', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('companions', models.ManyToManyField(related_name='going_on_trip', to='users.User')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips_created', to='users.User')),
                ('itinerary', models.ManyToManyField(related_name='part_of_trip', to='travels.Location')),
                ('transportation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transportation_for', to='travels.Transportation')),
            ],
        ),
    ]
