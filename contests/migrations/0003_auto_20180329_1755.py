# Generated by Django 2.0.2 on 2018-03-29 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_problem'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='in_practice',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='challenge',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='contests.Challenge'),
        ),
    ]