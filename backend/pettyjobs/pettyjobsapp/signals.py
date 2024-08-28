from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Job
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Job)
def job_saved(sender, instance, created, **kwargs):
    event_type = 'job_created' if created else 'job_updated'
    print(f"[DEBUG] Job {event_type} signal received for: {instance.title}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'jobs_{instance.job_type}',
        {
            'type': event_type,
            'job': {
                'id': instance.id,
                'title': instance.title,
                'job_type': instance.job_type,
                'location': instance.location,
                'description': instance.description,
                'status': instance.status,
                'criticality': instance.criticality,
                'approved_by': instance.approved_by.username if instance.approved_by else None,
                'accepted_by': instance.accepted_by.username if instance.accepted_by else None,
                'uploaded_by': instance.uploaded_by.username if instance.uploaded_by else None,
                'uploaded_at': instance.uploaded_at.isoformat(),
                'approved_at': instance.approved_at.isoformat() if instance.approved_at else None,
                'completed_at': instance.completed_at.isoformat() if instance.completed_at else None,
            }
        }
    )

@receiver(post_delete, sender=Job)
def job_deleted(sender, instance, **kwargs):
    print(f"[DEBUG] Job deleted signal received for: {instance.title}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'jobs_{instance.job_type}',
        {
            'type': 'job_deleted',
            'job': {
                'id': instance.id,
                'job_type': instance.job_type,
            }
        }
    )
