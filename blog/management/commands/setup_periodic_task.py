from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule

class Command(BaseCommand):
    help = 'Setup periodic task for creating blog posts'

    def handle(self, *args, **options):
        # Create interval schedule for every 10 minutes
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.MINUTES,
        )

        # Create periodic task
        task, created = PeriodicTask.objects.get_or_create(
            name='Create Random Blog Post',
            task='blog.tasks.create_random_blog_post',
            interval=schedule,
            enabled=True,
        )

        if created:
            self.stdout.write(self.style.SUCCESS('Periodic task created'))
        else:
            self.stdout.write(self.style.SUCCESS('Periodic task already exists'))
