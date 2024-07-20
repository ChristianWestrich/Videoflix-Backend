import os
import subprocess


def convert_480p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_480p.mp4'
    cmd = 'c:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source,
                                                                                                               new_file_name)
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name


def convert_720p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_720p.mp4'
    cmd = 'c:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source,
                                                                                                               new_file_name)
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name


def convert_1080p(source):
    new_file_name = source.rsplit('.', 1)[0] + '_1080p.mp4'
    cmd = 'c:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source,
                                                                                                                new_file_name)
    subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return new_file_name
