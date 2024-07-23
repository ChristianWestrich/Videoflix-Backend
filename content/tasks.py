import os
import subprocess

from Videoflix.settings import MEDIA_ROOT
from content.models import Movie

ffmpeg_path = '/opt/homebrew/bin/ffmpeg' #your path for ffmpeg on mac
ffmpeg_path_windows = 'c:/usr/ffmpeg/bin/ffmpeg.exe'

def convert_480p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_480p.mp4'
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name


def convert_720p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_720p.mp4'
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name


def convert_1080p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_1080p.mp4'
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name


def convert_and_update_480p(instance_id, source):
    new_file_name = convert_480p(source)
    movie_instance = Movie.objects.get(id=instance_id)
    movie_instance.video_480p = new_file_name.replace(MEDIA_ROOT, '').replace('\\', '/')
    movie_instance.save()


def convert_and_update_720p(instance_id, source):
    new_file_name = convert_720p(source)
    movie_instance = Movie.objects.get(id=instance_id)
    movie_instance.video_720p = new_file_name.replace(MEDIA_ROOT, '').replace('\\', '/')
    movie_instance.save()


def convert_and_update_1080p(instance_id, source):
    new_file_name = convert_1080p(source)
    movie_instance = Movie.objects.get(id=instance_id)
    movie_instance.video_1080p = new_file_name.replace(MEDIA_ROOT, '').replace('\\', '/')
    movie_instance.save()