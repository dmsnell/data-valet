APP_AUTHOR = 'dmsnell'
APP_SLUG = 'valet'
APP_TITLE = 'Valet'
APP_VERSION = '1.0'
APP_DESCRIPTION = 'Manage audio transcription and processing pipelines.'

# Menu strings
CLEAR_RECENTLY_OPENED = 'Clear Recently Opened…'


def truncate_words(max_words, input_text, suffix='…'):
    words = input_text.split()
    if len(words) <= max_words:
        return input_text
    else:
        return ' '.join(words[:max_words]) + suffix
