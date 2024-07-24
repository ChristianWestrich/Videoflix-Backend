import subprocess

from Videoflix.settings import MEDIA_ROOT
from content.models import Movie

ffmpeg_path = 'c:/usr/ffmpeg/bin/ffmpeg.exe'  # Your path for ffmpeg on Windows

def convert_original(source):
    new_file_name = source.rsplit('.', 1)[0] + '_original.mp4'
    cmd = f'"{ffmpeg_path}" -i "{source}" -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name

def convert_480p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_480p.mp4'
    cmd = f'"{ffmpeg_path}" -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{new_file_name}"'
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
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

def convert_to_hls(source, resolution):
    new_file_name = source.rsplit('.', 1)[0] + f'_{resolution}.m3u8'
    cmd = (
        f'"{ffmpeg_path}" -i "{source}" -c:v libx264 -crf 23 -c:a aac -strict -2 '
        f'-start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{new_file_name}"'
    )
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name

def convert_and_update(instance_id, source):
    resolutions = ['original', '480p', '720p', '1080p']
    hls_files = {}

    for res in resolutions:
        if res == 'original':
            new_file_name = convert_original(source)
        elif res == '480p':
            new_file_name = convert_480p(source)
        elif res == '720p':
            new_file_name = convert_720p(source)
        elif res == '1080p':
            new_file_name = convert_1080p(source)

        hls_file = convert_to_hls(new_file_name, res)
        hls_files[res] = hls_file.replace(MEDIA_ROOT, '').replace('\\', '/')

    movie_instance = Movie.objects.get(id=instance_id)
    movie_instance.video_file = hls_files['original']
    movie_instance.video_480p = hls_files['480p']
    movie_instance.video_720p = hls_files['720p']
    movie_instance.video_1080p = hls_files['1080p']
    movie_instance.save()
