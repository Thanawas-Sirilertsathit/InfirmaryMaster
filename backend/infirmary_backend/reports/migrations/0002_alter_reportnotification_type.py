from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportnotification',
            name='type',
            field=models.CharField(
                choices=[
                    ('low_stock', 'Low Stock'),
                    ('out_of_stock', 'Out Of Stock'),
                    ('expiring_batch', 'Expiring Batch'),
                ],
                max_length=32,
            ),
        ),
    ]