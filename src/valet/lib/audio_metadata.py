from dataclasses import dataclass


@dataclass
class AudioMeta:
    codecName: str
    duration: float
    sha1: bytes