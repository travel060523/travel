# Generated by Django 4.1.2 on 2023-04-30 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datec', models.DateTimeField(auto_now_add=True, verbose_name='datec_claim')),
                ('start', models.DateTimeField(verbose_name='start')),
                ('finish', models.DateTimeField(verbose_name='finish')),
                ('details', models.TextField(verbose_name='claim_details')),
                ('result', models.TextField(blank=True, null=True, verbose_name='result')),
            ],
            options={
                'db_table': 'claim',
                'ordering': ['datec'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='country_title')),
                ('details', models.TextField(verbose_name='country_details')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='country_photo')),
            ],
            options={
                'db_table': 'country',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='hotel_title')),
                ('details', models.TextField(verbose_name='hotel_details')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='hotel_photo')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='price')),
                ('flight', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='flight_cost')),
            ],
            options={
                'db_table': 'hotel',
                'ordering': ['region', 'title'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daten', models.DateTimeField(verbose_name='daten')),
                ('title', models.CharField(max_length=256, verbose_name='title_news')),
                ('details', models.TextField(verbose_name='details_news')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='photo_news')),
            ],
            options={
                'db_table': 'news',
                'ordering': ['daten'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dater', models.DateTimeField(auto_now_add=True, verbose_name='dater_reviews')),
                ('rating', models.IntegerField(blank=True, null=True, verbose_name='rating')),
                ('details', models.TextField(verbose_name='details_reviews')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_hotel', to='kaz.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reviews',
                'ordering': ['dater'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='region_title')),
                ('details', models.TextField(verbose_name='region_details')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region_country', to='kaz.country')),
            ],
            options={
                'db_table': 'region',
                'ordering': ['country', 'title'],
            },
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['daten'], name='news_daten_a29edb_idx'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotel_region', to='kaz.region'),
        ),
        migrations.AddIndex(
            model_name='country',
            index=models.Index(fields=['title'], name='country_title_3c5f39_idx'),
        ),
        migrations.AddField(
            model_name='claim',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claim_hotel', to='kaz.hotel'),
        ),
        migrations.AddField(
            model_name='claim',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claim_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddIndex(
            model_name='reviews',
            index=models.Index(fields=['dater'], name='reviews_dater_c1460a_idx'),
        ),
        migrations.AddIndex(
            model_name='region',
            index=models.Index(fields=['country', 'title'], name='region_country_0d40d3_idx'),
        ),
        migrations.AddIndex(
            model_name='hotel',
            index=models.Index(fields=['region', 'title'], name='hotel_region__880898_idx'),
        ),
        migrations.AddIndex(
            model_name='claim',
            index=models.Index(fields=['datec', 'user'], name='claim_datec_7b225b_idx'),
        ),
    ]