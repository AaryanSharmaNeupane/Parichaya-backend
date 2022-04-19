from .models import ShareLink
from celery import shared_task
from django_celery_beat.models import PeriodicTask, CrontabSchedule, ClockedSchedule


@shared_task
def delete_share_link(share_link_id, scheduler_id):
    share_link = ShareLink.objects.get(id=share_link_id)
    scheduler = ClockedSchedule.objects.get(id=scheduler_id)
    share_link.delete()
    scheduler.delete()
