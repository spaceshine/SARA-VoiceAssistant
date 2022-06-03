import os
import torch
import wave
import contextlib
from pydub import AudioSegment
from pydub.playback import play

from tts_utils import apply_tts  # modify these utils and use them your project


class SileroTTS:
    def __init__(self):
        torch.set_grad_enabled(False)
        self.device = torch.device('cpu')
        torch.set_num_threads(4)
        self.symbols = '_~абвгдеёжзийклмнопрстуфхцчшщъыьэюя +.,!?…:;–'
        local_file = 'model.jit'

        self.model = torch.jit.load(local_file, map_location=self.device)
        self.model.eval()
        for param in self.model.parameters():
            param.grad = None
        self.model = self.model.to(self.device)
        self.sample_rate = 16000
        self.__isrunning = True

    def say(self, texts):
        print("In say")
        audio = apply_tts(texts=texts,
                          model=self.model,
                          sample_rate=self.sample_rate,
                          symbols=self.symbols,
                          device=self.device)
        print("model worked")
        for i, _audio in enumerate(audio):
            write_wave(path=f'test_{str(i).zfill(3)}.wav',
                       audio=(audio[i] * 32767).numpy().astype('int16'),
                       sample_rate=16000)
            print("wav saved")
            sound = AudioSegment.from_wav(f'test_{str(i).zfill(3)}.wav')
            play(sound)

    def isrunning(self):
        return self.__isrunning

    def assistant_quit(self):
        self.__isrunning = False


def write_wave(path, audio, sample_rate):
    """Writes a .wav file.
    Takes path, PCM audio data, and sample rate.
    """
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)
