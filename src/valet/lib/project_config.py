import os


class ProjectConfig:
    baseDirectory: os.PathLike
    configName: os.PathLike
    sourceDirectory: os.PathLike
    transcriptionDirectory: os.PathLike
    liwksConfigName: os.PathLike
    outputName: os.PathLike

    def __init__(self, baseDirectory):
        """
        Create default config.

        todo: It would be good to allow modification of the config parameters.
              This isn’t implemented at the present time though because it’s not
              entirely clear that it would be necessary.

        :param baseDirectory: Project root directory.
        """
        self.baseDirectory = baseDirectory
        self.configDirectory = '.valet'
        self.sourceDirectory = 'source-audio'
        self.transcriptionDirectory = 'transcripts'
        self.liwksConfigName = 'liwks-input.csv'
        self.outputName = 'features.csv'