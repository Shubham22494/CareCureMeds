# Generated by Django 5.0.3 on 2024-03-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('medicine_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expiry_date', models.DateField()),
                ('type', models.CharField(choices=[('Tablet', 'Tablet'), ('Capsule', 'Capsule'), ('Liquid', 'Liquid'), ('Injection', 'Injection'), ('Cream', 'Cream'), ('Ointment', 'Ointment'), ('Drops', 'Drops'), ('Inhaler', 'Inhaler'), ('Powder', 'Powder'), ('Other', 'Other')], max_length=20)),
                ('prescription_required', models.BooleanField()),
            ],
        ),
    ]
