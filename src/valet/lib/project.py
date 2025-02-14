import pathlib
import os
import os.path

import valet.lib.human as human
import valet.lib.ffmpeg as ffmpeg
import valet.lib.whisper as whisper
from valet.lib.project_config import ProjectConfig


class Project:
    config: ProjectConfig

    @classmethod
    def open_existing(cls, config):
        """
        :param ProjectConfig config:
        """
        baseDirectory = pathlib.Path(config.baseDirectory)
        [
            pathlib.Path(baseDirectory, dir).mkdir(parents=True, exist_ok=True)
            for dir in [
                config.configDirectory,
                config.sourceDirectory,
                config.transcriptionDirectory
            ]
        ]

        project = Project()
        project.config = config
        return project

    @classmethod
    def available_actions(cls):
        return [
            'list-sources',
            'transcribe',
            'run'
        ]

    def run(self, action):
        match action:
            case 'list-sources':
                for file, meta in self.get_source_files().items():
                    print(f"{os.path.basename(file)}: {meta.codecName.upper()} {human.duration(meta.duration)}")

            case 'transcribe':
                self.generate_transcriptions()

            case 'run' | _:
                self.generate_transcriptions()

    def get_source_files(self):
        sourceDir = pathlib.Path(self.config.baseDirectory, self.config.sourceDirectory)
        sources   = dict()

        for file in sourceDir.iterdir():
            meta = ffmpeg.get_meta_for_file(file)
            if meta is None:
                continue

            sources[file] = meta

        return sources

    def generate_transcriptions(self):
        for file in self.get_source_files().keys():
            transcriptFile = pathlib.Path(self.config.baseDirectory, self.config.transcriptionDirectory, os.path.basename(file))
            if not transcriptFile.exists():
                transcript = self.transcribe(str(file))
                transcriptFile.write_text(transcript)
            else:
                print(f"\x1b[90mTranscript '\x1b[2;33m{transcriptFile}\x1b[0;90m' already exists.\x1b[m")

    def transcribe(self, file):
        print(f"\x1b[90mTranscribing '\x1b[2;33m{file}\x1b[0;90m'\x1b[m")
        return whisper.transcribe(file)

    def available_sources(self):
        sourceDir = pathlib.Path(self.config.baseDirectory, self.config.sourceDirectory)
        for file in sourceDir.iterdir():
            yield file
