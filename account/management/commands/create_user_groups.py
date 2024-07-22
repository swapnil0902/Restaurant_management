from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **kwargs):
        groups_permissions = {
            'Customer ': ['view_customer', 'change_customer', 'add_customer', 'delete_customer', 'view_menuitem', 'view_order', 'change_order', 'add_order', 'delete_order'],
            'Restaurant Owner': ['view_menuitem', 'change_menuitem', 'add_menuitem', 'delete_menuitem', 'view_customer', 'view_order'],
            'Manager': ['view_customer', 'change_customer', 'add_customer', 'delete_customer', 'view_menuitem', 'change_menuitem', 'add_menuitem', 'delete_menuitem', 'view_order', 'change_order', 'add_order', 'delete_order'],
        }

        # Create groups and assign permissions
        for group_name, permission_codenames in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Created group: {group_name}')
            else:
                self.stdout.write(f'Group already exists: {group_name}')

            # Assign permissions to the group
            for codename in permission_codenames:
                try:
                    content_type = self.get_content_type(codename)
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    group.permissions.add(permission)
                    self.stdout.write(f'Permission {codename} added to group {group_name}')
                except Permission.DoesNotExist:
                    self.stderr.write(f'Permission {codename} does not exist.')

        self.stdout.write(self.style.SUCCESS('Successfully created user groups and assigned permissions.'))

    def get_content_type(self, codename):
        if 'customer' in codename:
            app_label = 'customer'  # Adjust based on your app
            model = 'customer'
        elif 'order' in codename:
            app_label = 'order'  # Adjust based on your app
            model = 'order'
        elif 'menuitem' in codename:
            app_label = 'menu'  # Adjust based on your app
            model = 'menuitem'
        else:
            raise ValueError(f'Unknown codename: {codename}')
        
        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
        except ContentType.DoesNotExist:
            raise ValueError(f'ContentType not found for {app_label}.{model}')
        
        return content_type
