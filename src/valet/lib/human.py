import math


def duration(seconds):
    segments = []

    if seconds > 86400:
        segments.append(f"{math.floor(seconds / 86400)}years")
        seconds -= math.floor(seconds / 86400) * 86400

    if seconds > 30 * 24 * 3600:
        segments.append(f"{math.floor(seconds / (30 * 24 * 3600))}months")
        seconds -= math.floor(seconds / (30 * 24 * 3600)) * 30 * 24 * 3600

    if seconds > 24 * 3600:
        segments.append(f"{math.floor(seconds / (24 * 3600))}days")
        seconds -= math.floor(seconds / (24 * 3600)) * 24 * 3600

    if seconds > 3600:
        segments.append(f"{math.floor(seconds / 3600)}h")
        seconds -= math.floor(seconds / 3600) * 3600

    if seconds > 60:
        segments.append(f"{math.floor(seconds / 60)}m")
        seconds -= math.floor(seconds / 60) * 60

    if seconds >=1:
        segments.append(f"{math.floor(seconds)}s")
        seconds -= math.floor(seconds)

    if seconds > 0:
        segments.append(f"{math.floor(seconds * 1000)/1000}ms")

    return ' '.join(segments)


def file_size(bytes):
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    index = 0
    while bytes >= 1024 and index < len(units) - 1:
        bytes /= 1024
        index += 1
    if index == 0:
        return f"{int(bytes)} {units[index]}"
    else:
        return f"{bytes:.2f} {units[index]}"
