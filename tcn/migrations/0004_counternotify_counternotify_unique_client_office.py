# Generated by Django 5.0.6 on 2024-06-30 01:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcn', '0003_alter_window_number_of_served_tickets'),
    ]

    operations = [
        migrations.CreateModel(
            name='CounterNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counter_notifications', to=settings.AUTH_USER_MODEL)),
                ('office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counter_notifications', to='tcn.office')),
            ],
        ),
        migrations.AddConstraint(
            model_name='counternotify',
            constraint=models.UniqueConstraint(fields=('client', 'office'), name='unique_client_office'),
        ),
    ]
