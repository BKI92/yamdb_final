# Generated by Django 3.0.5 on 2020-06-22 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_auto_20200622_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.PROTECT,
                                    related_name='titles', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(blank=True),
        ),
    ]
