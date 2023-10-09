# Generated by Django 4.1.5 on 2023-10-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_alter_e_cart_e_commerce_alter_e_commerce_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="e_category", name="name", field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="e_commerce",
            name="title",
            field=models.CharField(max_length=40, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="e_composition",
            name="name",
            field=models.CharField(max_length=16),
        ),
    ]
