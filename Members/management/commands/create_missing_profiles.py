from django.core.management.base import BaseCommand
from Members.models import Members, Profile  # Replace 'your_app'

class Command(BaseCommand):
    help = 'Creates missing profiles for Members'

    def handle(self, *args, **options):
        members_without_profile = Members.objects.filter(profile__isnull=True)
        count = members_without_profile.count()
        if count > 0:
            self.stdout.write(self.style.WARNING(f'Found {count} Members without a Profile.'))
            for member in members_without_profile:
                Profile.objects.create(user=member)
                self.stdout.write(self.style.SUCCESS(f'Created profile for member: {member}'))
            self.stdout.write(self.style.SUCCESS('Successfully created missing profiles.'))
        else:
            self.stdout.write(self.style.SUCCESS('All Members already have a Profile.'))
