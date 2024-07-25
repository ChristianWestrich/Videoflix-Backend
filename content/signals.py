import os
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from .models import Movie
import django_rq
from content.tasks import convert_and_update, delete_original_file

@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_and_update, instance.id, instance.video_file.path, '480p')
        queue.enqueue(convert_and_update, instance.id, instance.video_file.path, '720p')
        queue.enqueue(convert_and_update, instance.id, instance.video_file.path, '1080p')

@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
    for resolution in ['480p', '720p', '1080p']:
        video_attr = getattr(instance, f'video_{resolution}', None)
        if video_attr:
            video_path = os.path.join(settings.MEDIA_ROOT, video_attr.strip('/'))
            if os.path.isfile(video_path):
                os.remove(video_path)

