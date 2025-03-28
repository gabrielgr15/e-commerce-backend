# Generated by Django 5.1.7 on 2025-03-24 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('description', models.TextField()),
                ('categories', models.ManyToManyField(related_name='list_products', to='products.category')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(related_name='list_categories', to='products.product'),
        ),
    ]
