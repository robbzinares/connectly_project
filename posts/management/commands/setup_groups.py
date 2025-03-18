from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User

class Command(BaseCommand):
    help = "Create default user groups and assign users"

    def handle(self, *args, **kwargs):
        # Create 'Admin' group if it doesn't exist
        admin_group, created = Group.objects.get_or_create(name="Admin")
        if created:
            self.stdout.write(self.style.SUCCESS("Admin group created."))

        # Check if user exists, otherwise create it
        user, user_created = User.objects.get_or_create(username="admin_user")
        if user_created:
            user.set_password("admin123")  # Set a default password
            user.save()
            self.stdout.write(self.style.SUCCESS("User 'admin_user' created."))

        # Assign user to the 'Admin' group
        user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f"User {user.username} added to Admin group."))