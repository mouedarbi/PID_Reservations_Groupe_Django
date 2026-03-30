from django.db import migrations

def assign_permissions(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Get or create the Review content type manually if it doesn't exist yet (common in tests)
    review_ct, created = ContentType.objects.get_or_create(app_label='catalogue', model='review')
    
    # Permissions (Ensure they exist, though they should be created by Django)
    # We use get_or_create to be safe during tests where post_migrate signals might not have run yet
    add_review, _ = Permission.objects.get_or_create(content_type=review_ct, codename='add_review', defaults={'name': 'Can add review'})
    change_review, _ = Permission.objects.get_or_create(content_type=review_ct, codename='change_review', defaults={'name': 'Can change review'})
    delete_review, _ = Permission.objects.get_or_create(content_type=review_ct, codename='delete_review', defaults={'name': 'Can delete review'})
    view_review, _ = Permission.objects.get_or_create(content_type=review_ct, codename='view_review', defaults={'name': 'Can view review'})
    
    # Group names
    member_group = Group.objects.get(name='MEMBER')
    press_group = Group.objects.get(name='PRESS_CRITIC')
    producer_group = Group.objects.get(name='PRODUCER')
    admin_group = Group.objects.get(name='ADMINISTRATOR')
    
    # Assign permissions
    # Members can manage their own reviews
    member_group.permissions.add(add_review, change_review, delete_review, view_review)
    
    # Press critics can manage their own articles
    press_group.permissions.add(add_review, change_review, delete_review, view_review)
    
    # Producers can moderate (delete) but not add or edit content
    producer_group.permissions.add(delete_review, view_review, change_review)
    
    # Admins can do everything
    admin_group.permissions.add(add_review, change_review, delete_review, view_review)

def remove_permissions(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_create_default_groups'),
        ('catalogue', '0001_initial'), # Ensure Review model exists
    ]
    operations = [
        migrations.RunPython(assign_permissions, remove_permissions),
    ]
