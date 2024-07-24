import os
from django.dispatch import receiver
from .models import Movie
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Movie)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue('content.tasks.convert_and_update', instance.id, instance.video_file.path)

@receiver(post_delete, sender=Movie)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
        file_root, file_ext = os.path.splitext(instance.video_file.path)
        converted_files = [f"{file_root}_original.mp4", f"{file_root}_480p.mp4", f"{file_root}_720p.mp4", f"{file_root}_1080p.mp4"]

        for file in converted_files:
            if os.path.isfile(file):
                os.remove(file)
