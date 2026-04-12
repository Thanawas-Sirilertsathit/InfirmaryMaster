from django.db import migrations, models


def set_initial_verified_values(apps, schema_editor):
    User = apps.get_model('users', 'User')
    User.objects.filter(role='staff').update(verified=False)
    User.objects.exclude(role='staff').update(verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verified',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(set_initial_verified_values, migrations.RunPython.noop),
    ]