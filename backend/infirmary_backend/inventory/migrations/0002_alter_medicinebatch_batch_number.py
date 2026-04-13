from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicinebatch',
            name='batch_number',
            field=models.CharField(blank=True, max_length=64, unique=True),
        ),
    ]
