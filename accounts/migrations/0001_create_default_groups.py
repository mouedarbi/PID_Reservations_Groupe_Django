from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    groups = [
        'MEMBER',
        'AFFILIATE',
        'PRESS_CRITIC',
        'PRODUCER',
        'ADMINISTRATOR',
    ]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]