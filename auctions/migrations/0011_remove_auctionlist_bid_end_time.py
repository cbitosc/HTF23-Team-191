# Generated by Django 4.2.1 on 2023-10-07 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auctionlist_daysleft'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlist',
            name='bid_end_time',
        ),
    ]
