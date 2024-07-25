import os
import subprocess
from django.conf import settings
from content.models import Movie

ffmpeg_path = '/opt/homebrew/bin/ffmpeg'  # Pfad zu ffmpeg auf Mac
ffmpeg_path_windows = 'c:/usr/ffmpeg/bin/ffmpeg.exe'  # Pfad zu ffmpeg auf Windows

def convert_to_hls(source, resolution):
    resolutions = {
        '480p': 'hd480',
        '720p': 'hd720',
        '1080p': 'hd1080'
    }
    base_name = os.path.splitext(os.path.basename(source))[0]
    output_file = os.path.join(settings.MEDIA_ROOT, 'videos', f"{base_name}_{resolution}.m3u8")

    cmd = f'"{ffmpeg_path}" -i "{source}" -vf scale={resolutions[resolution]} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{output_file}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

    return output_file

def convert_and_update(instance_id, source, resolution):
    new_file_name = convert_to_hls(source, resolution)
    movie_instance = Movie.objects.get(id=instance_id)
    setattr(movie_instance, f'video_{resolution}', new_file_name.replace(settings.MEDIA_ROOT, '').replace('\\', '/'))
    movie_instance.save()

def delete_original_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
