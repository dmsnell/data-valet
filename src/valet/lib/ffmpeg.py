import json
import pathlib
import shutil
import subprocess
from json import JSONDecodeError

from . import audio_metadata, hashing


def get_binary_path():
    match shutil.which('ffmpeg'):
        case str(path):
            return pathlib.Path(path)

        case None:
            return None


def get_meta_for_file(filepath):
    """
    :param pathlib.Path filepath:
    """
    response = subprocess.run([
        'ffprobe',
        '-loglevel', 'quiet',
        '-show_entries', 'stream=codec_name,codec_type,duration',
        '-of', 'json',
        str(filepath)
    ], capture_output=True)

    if 0 != response.returncode:
        return None

    try:
        data = json.loads(response.stdout)
    except JSONDecodeError:
        return None

    if 'streams' not in data:
        return None

    audio_stream = next(stream for stream in data['streams'] if 'codec_type' in stream and 'audio' == stream['codec_type'])
    if not audio_stream:
        return None

    return audio_metadata.AudioMeta(
        codecName = audio_stream['codec_name'] if 'codec_name' in audio_stream else 'unknown',
        duration  = float_or(audio_stream['duration'] if 'duration' in audio_stream else '', 0),
        sha1      = hashing.file_hash(filepath, 'sha1')
    )


def float_or(to_parse, default_value):
    try:
        return float(to_parse)
    except ValueError:
        return default_value