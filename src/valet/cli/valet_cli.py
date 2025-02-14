import argparse
import pathlib
import os

import whisper

import valet.lib.project_config
from valet.lib.project import Project
from valet.lib import strings as i18n

def main():
    args = arg_parser().parse_args()

    try:
        config = args_to_config(args)
        project = Project.open_existing(config)

        project.run(args.action)

    except ValueError as e:
        print(arg_parser(epilog=str(e)).format_help())


def arg_parser(**argumentParserArgs):
    parser = argparse.ArgumentParser(
        prog=i18n.APP_SLUG,
        description=i18n.APP_DESCRIPTION,
        **argumentParserArgs
    )
    parser.add_argument('-d', '--project-path', type=pathlib.Path, help='Base directory for the project')

    action_group = parser.add_argument_group('Project Actions', 'What do you want to do? Choose only one')
    action_choice = action_group.add_mutually_exclusive_group()
    action_choice.add_argument('-l', '--list-sources', dest='action', action='store_const', const='list-sources', help='List the potential audio input sources.')
    action_choice.add_argument('-t', '--transcribe', dest='action', action='store_const', const='transcribe', help='Transcribe all available audio inputs.')

    whisper_options = parser.add_argument_group('whisper options', 'Options for the OpenAI Whisper transcriber.')
    whisper_options.add_argument('-m', '--model', help='Which model to use when transcribing', choices=whisper.available_models())

    return parser


def args_to_config(args):
    if args.project_path is None:
        raise ValueError('Supply --project-path=PROJECT_ROOT to specify where to run the pipeline.')

    if not os.path.isdir(args.project_path):
        raise ValueError("""
            Path supplied to --project-path must exist.
            Check for typos, or create directory before running.
            E.g. `mkdir ~/path/to/project`
        """)

    return valet.lib.project_config.ProjectConfig(args.project_path)