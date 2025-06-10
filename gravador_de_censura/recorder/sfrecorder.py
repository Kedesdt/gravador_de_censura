import soundfile as sf
import numpy as np
import queue
import time
import threading
import traceback
import os
from util.util import save


class SFRecorder(threading.Thread):
    def __init__(
        self,
        sd_input,
        output_file="gravacao.mp3",
        duration=10,
        directory=".",
        daemon=True,
    ):
        super().__init__(daemon=daemon)
        self.sd_input = sd_input  # Instância de SDInput
        self.output_file = output_file
        self.duration = duration
        self.frames = []
        self.writer = None
        self.dir = directory
        self.running = True
        self.recording = False

    def run(self):
        while self.running:
            time.sleep(1)
            while self.recording:
                try:
                    self.record()
                except:
                    traceback.print_exc()

        print("Recorder terminado")
        if self.writer:
            self.writer.set_running(False)
        self.writer.join()
        self.writer = None

    def set_running(self, b):
        self.running = b

    def set_recording(self, b):
        self.recording = b

    def start_record(self):
        self.writer = SFRecorder_Writer(daemon=True)
        self.writer.start()
        self.recording = True

    def stop_record(self):

        self.recording = False

    def generate_name(self):

        name = (
            time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            + "-"
            + self.output_file
        )
        path = os.path.join(self.dir, name)

        return path

    def record(self):

        start_time = time.time()

        while time.time() - start_time < self.duration:
            try:
                data = self.sd_input.queue.get(timeout=self.sd_input.timeout)
                self.frames.append(data)
            except queue.Empty:
                print("Fila vazia, encerrando gravação.")
                break

        # Convertendo os frames para um único array
        audio_data = np.concatenate(self.frames, axis=0)

        # Salvando como WAV usando soundfile
        data = {"name": self.generate_name(), "data": audio_data}
        self.writer.add(data)

        self.frames = []


class SFRecorder_Writer(threading.Thread):

    def __init__(self, delay=1, samplerate=44100, daemon=True):
        super().__init__(daemon=daemon)
        self.queue = queue.Queue()
        self.delay = delay
        self.samplerate = samplerate
        self.running = True

    def run(self):
        while self.running:

            try:
                try:
                    data = self.queue.get(timeout=self.delay)
                    save(data["name"], data["data"], self.samplerate)
                except queue.Empty:

                    time.sleep(self.delay)
                # sf.write(self.generate_name(), audio_data, samplerate=44100)

            except Exception as e:
                traceback.print_exc()

        print("writer terminado")

    def add(self, data):
        self.queue.put(data)

    def set_running(self, b):
        self.running = b
