# Generated by Django 3.2 on 2021-07-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_alter_crypto_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crypto',
            name='change',
            field=models.FloatField(default=0),
        ),
    ]