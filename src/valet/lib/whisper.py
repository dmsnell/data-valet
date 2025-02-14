import torch
import whisper

# Disable console warnings about weights_only
# https://github.com/openai/whisper/pull/2451
import functools
whisper.torch.load = functools.partial(whisper.torch.load, weights_only=True)

def transcribe(filepath, model_name='tiny'):
    """
    Produce a transcription of an input audio file given its full path.

    :param filepath: Full path to input audio file, of any format supported by ffmpeg.
    :param model_name: See OpenAI-Whisper project for possible model names.
    :return:
    """

    # Apple Silicon chips support the `mps` backend for `torch`, but it
    # fails when running transcription on some unsupported feature. Allow
    # it with the following if doing so completes without error.
    #
    # ```
    # 'mps' if torch.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu'
    # ```
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    # When running on a CPU the FP16 functionality may not work, in which case
    # it will fall back to FP32, but display a warning message in the console.
    fp16 = torch.cuda.is_available()

    model = whisper.load_model(model_name, device=device)
    result = model.transcribe(filepath, verbose=None, fp16=fp16)
    return result['text']
