# Generated by Django 4.0.6 on 2022-07-20 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_supportedmeasure_calculatedmeasure'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectedmetric',
            name='path',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='collectedmetric',
            name='qualifier',
            field=models.CharField(blank=True, default=None, max_length=5, null=True),
        ),
    ]
