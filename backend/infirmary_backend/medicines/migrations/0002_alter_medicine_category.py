from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.CharField(max_length=128),
        ),
    ]
