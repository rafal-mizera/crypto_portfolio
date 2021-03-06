# Generated by Django 3.2 on 2021-07-01 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='cryptos',
        ),
        migrations.AddField(
            model_name='portfolio',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='crypto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.crypto'),
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
