# Generated by Django 5.1.1 on 2024-10-24 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_variation_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='count',
        ),
        migrations.AlterField(
            model_name='variation',
            name='category',
            field=models.CharField(choices=[('Color', 'Color'), ('Size', 'Size'), ('Material', 'Material')], max_length=100),
        ),
    ]
