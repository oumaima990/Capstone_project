# Generated by Django 5.0.6 on 2024-11-26 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0008_alter_question_node'),
    ]

    operations = [
        migrations.AddField(
            model_name='text',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='text_images/'),
        ),
    ]
