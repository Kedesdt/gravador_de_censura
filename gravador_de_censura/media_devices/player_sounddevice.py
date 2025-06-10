import traceback
import sounddevice as sd
import soundfile as sf
import queue
import sys
import numpy

from config import (
    INPUT_GAIN,
    OUTPUT_GAIN,
    BLOCK_SIZE,
    BUFFER_SIZE,
    SAMPLE_RATE,
    CHANNELS,
)


class SDInput:

    def __init__(
        self, device=0, player=None, audio_commander=None, master=None, gain=INPUT_GAIN
    ):

        self.gain = 10 ** (gain / 20)
        self.master = master
        self.audio_commander = audio_commander
        self.player = player
        self.playing = False
        self.queue = queue.Queue()
        self.medias_playing = []
        self.device = device
        self.streaming_resetting = False
        self.vu = None
        self.timeout = BLOCK_SIZE * BUFFER_SIZE / SAMPLE_RATE
        self.vu_value = (0, 0)
        try:
            self.stream = sd.InputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                device=self.device,
                channels=2,
                callback=self.input_callback,
            )

            self.stream.start()
        except Exception as e:
            print("impossibilitado de criar input")
            self.stream = None
            traceback.print_exc()

        print("Input Device: ", self.device)

    def input_callback(self, indata, frames, time, status):

        data = numpy.zeros((BLOCK_SIZE, CHANNELS))
        data[:] = indata * self.gain
        if self.vu:
            self.vu_value = numpy.amax(data, 0)
        if self.queue:
            self.queue.put(data, timeout=self.timeout)

    def set_vu(self, b):
        self.vu = b

    def stop(self):
        self.vu_value = (0, 0)
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
                print("InputStream parado e fechado.")
            except Exception as e:
                print("Erro ao parar InputStream:", e)
