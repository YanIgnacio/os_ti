# Generated by Django 4.2.5 on 2023-10-05 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os_ti', '0004_ordemdeservico_secretaria_ordemdeservico_setor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordemdeservico',
            name='secretaria',
            field=models.CharField(default='', max_length=100, verbose_name='Secretaria'),
        ),
        migrations.AlterField(
            model_name='ordemdeservico',
            name='setor',
            field=models.CharField(default='', max_length=100, verbose_name='Setor'),
        ),
    ]
