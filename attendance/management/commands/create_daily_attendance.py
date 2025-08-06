from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from attendance.models import AttendanceStatus
from datetime import date

class Command(BaseCommand):
    help = 'Create daily attendance status records for all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Date in YYYY-MM-DD format (default: today)',
        )

    def handle(self, *args, **options):
        target_date = options['date']
        if target_date:
            try:
                target_date = date.fromisoformat(target_date)
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
                )
                return
        else:
            target_date = date.today()

        # Get all active users (excluding superusers)
        users = User.objects.filter(is_active=True).exclude(is_superuser=True)
        
        created_count = 0
        updated_count = 0
        
        for user in users:
            attendance_status, created = AttendanceStatus.objects.get_or_create(
                user=user,
                date=target_date,
                defaults={'status': 'absent'}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    f'Created attendance status for {user.username} on {target_date}'
                )
            else:
                updated_count += 1
                self.stdout.write(
                    f'Attendance status already exists for {user.username} on {target_date}'
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed {len(users)} users. '
                f'Created: {created_count}, Updated: {updated_count}'
            )
        ) 