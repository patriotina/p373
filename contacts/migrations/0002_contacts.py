# Generated by Django 2.0.4 on 2018-05-08 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_data', models.CharField(max_length=200)),
                ('persona_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='contacts.Names')),
            ],
        ),
    ]
