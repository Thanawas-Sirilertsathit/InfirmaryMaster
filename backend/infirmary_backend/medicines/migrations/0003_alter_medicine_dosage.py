from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0002_alter_medicine_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='dosage',
            field=models.CharField(max_length=128),
        ),
    ]
