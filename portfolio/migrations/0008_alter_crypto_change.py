# Generated by Django 3.2 on 2021-07-19 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_auto_20210719_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='change',
            field=models.FloatField(blank=True),
        ),
    ]
