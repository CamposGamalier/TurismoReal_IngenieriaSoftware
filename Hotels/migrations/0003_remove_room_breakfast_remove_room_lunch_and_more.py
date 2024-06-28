# Generated by Django 5.0.6 on 2024-06-27 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotels', '0002_room'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='breakfast',
        ),
        migrations.RemoveField(
            model_name='room',
            name='lunch',
        ),
        migrations.RemoveField(
            model_name='room',
            name='reserve_date',
        ),
        migrations.RemoveField(
            model_name='room',
            name='tour_guide',
        ),
        migrations.RemoveField(
            model_name='room',
            name='transportation',
        ),
        migrations.AddField(
            model_name='room',
            name='price_per_night',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]