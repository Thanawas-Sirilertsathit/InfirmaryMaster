from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0002_alter_medicinebatch_batch_number'),
        ('medicines', '0003_alter_medicine_dosage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('low_stock', 'Low Stock'), ('expiring_batch', 'Expiring Batch')], max_length=32)),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_notifications', to='inventory.medicinebatch')),
                ('medicine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='report_notifications', to='medicines.medicine')),
            ],
            options={
                'ordering': ['is_read', '-created_at'],
            },
        ),
    ]