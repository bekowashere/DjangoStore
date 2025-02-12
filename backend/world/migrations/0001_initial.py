# Generated by Django 5.1.1 on 2024-09-29 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency_code', models.CharField(max_length=3, verbose_name='Currency Code')),
                ('currency_name', models.CharField(max_length=64, verbose_name='Currency Name')),
                ('currency_symbol', models.CharField(max_length=8, verbose_name='Currency Symbol')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
                'ordering': ['currency_name'],
            },
        ),
        migrations.CreateModel(
            name='Timezone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zoneName', models.CharField(max_length=64, verbose_name='Timezone Name')),
                ('gmtOffset', models.CharField(max_length=8)),
                ('gmtOffsetName', models.CharField(max_length=16)),
                ('abbreviation', models.CharField(max_length=4)),
                ('tzName', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Timezone',
                'verbose_name_plural': 'Timezones',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Country Name')),
                ('iso3', models.CharField(max_length=3, verbose_name='ISO3')),
                ('iso2', models.CharField(max_length=2, verbose_name='ISO2')),
                ('numeric_code', models.CharField(max_length=4, verbose_name='Numeric Code')),
                ('phone_code', models.CharField(max_length=8, verbose_name='Phone Code')),
                ('capital', models.CharField(max_length=64, verbose_name='Capital')),
                ('tld', models.CharField(max_length=8, verbose_name='TLD')),
                ('native', models.CharField(max_length=255, verbose_name='Native')),
                ('region', models.CharField(max_length=64, verbose_name='Region')),
                ('subregion', models.CharField(max_length=64, verbose_name='Sub Region')),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Latitude')),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11, verbose_name='Longitude')),
                ('emoji', models.CharField(max_length=2, verbose_name='Emoji')),
                ('emojiU', models.CharField(max_length=32, verbose_name='Emoji U')),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='currency_countries', to='world.currency')),
                ('timezones', models.ManyToManyField(blank=True, to='world.timezone', verbose_name='Timezones')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
    ]
