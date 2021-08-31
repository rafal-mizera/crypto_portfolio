# Generated by Django 3.2 on 2021-07-27 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_auto_20210719_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='updateportfolio',
            name='crypto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.crypto'),
        ),
        migrations.AddField(
            model_name='updateportfolio',
            name='portfolio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='portfolio.portfolio'),
        ),
        migrations.DeleteModel(
            name='PortfolioCrypto',
        ),
    ]