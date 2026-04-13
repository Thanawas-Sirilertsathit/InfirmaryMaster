from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0003_alter_medicine_dosage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MedicineCategory',
        ),
    ]