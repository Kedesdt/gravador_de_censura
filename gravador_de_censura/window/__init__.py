import tkinter as tk
from tkinter import filedialog
from vu.vertical_vu import Vu
from media_devices.player_sounddevice import SDInput
from recorder.sfrecorder import SFRecorder
import time
import sounddevice as sd
from tkinter import ttk


class MainWindow:

    def __init__(self, master, recorders=4):
        self.master = master
        self.recorders = recorders
        master.title("Gravador de Censura")

        self.dir_labels = {}
        self.dir_entries = {}
        self.dir_buttons = {}
        self.device_labels = {}
        self.device_entrys = {}
        self.start_buttons = {}
        self.stop_buttons = {}
        self.vu_frames = {}
        self.vus = {}
        self.sd_inputs = {}
        self.sd_recorders = {}
        self.device_comboboxs = {}
        self.recording = {i: False for i in range(self.recorders)}
        self.selected_directories = {i: "." for i in range(self.recorders)}
        self.selected_input_devices = {i: 0 for i in range(self.recorders)}

        for i in range(self.recorders):

            frame = tk.Frame(master)

            # Entrada para diretório
            dir_label = tk.Label(frame, text="Diretório:")
            self.dir_labels[i] = dir_label
            # dir_label.grid(row=0, column=0, sticky="e")
            dir_entry = tk.Entry(frame, width=20)
            self.dir_entries[i] = dir_entry
            dir_entry.grid(row=0, column=1)
            dir_button = tk.Button(
                frame, text="Selecionar", command=lambda x=i: self.select_directory(x)
            )
            self.dir_buttons[i] = dir_button
            dir_button.grid(row=1, column=1)

            # Entrada para device de áudio (Combobox)
            device_label = tk.Label(frame, text="Device de Áudio:")
            # device_label.grid(row=1, column=0, sticky="e")
            self.device_labels[i] = device_label
            device_combobox = ttk.Combobox(frame, width=37, state="readonly")
            device_combobox.grid(row=2, column=1, columnspan=2)
            self.device_comboboxs[i] = device_combobox
            self.populate_audio_devices(i)

            # Botão Start
            start_button = tk.Button(
                frame, text="Start", command=lambda x=i: self.start(x)
            )
            start_button.grid(row=3, column=1, sticky="ew")
            self.start_buttons[i] = start_button

            # Botão Stop
            stop_button = tk.Button(
                frame, text="Stop", command=lambda x=i: self.stop(x)
            )
            stop_button.grid(row=4, column=1, sticky="ew")
            self.stop_buttons[i] = stop_button

            # Vertical VU
            vu_frame = tk.Frame(frame)
            vu_frame.grid(row=5, column=1, pady=10)
            self.vu_frames[i] = vu_frame
            vu = Vu(frame, vu_frame, width=60, height=200, player=None, daemon=True)
            self.vus[i] = vu

            frame.pack(side="left")

    def populate_audio_devices(self, i):

        devices = sd.query_devices()
        input_devices = [d["name"] for d in devices if d["max_input_channels"] > 0]
        self.device_comboboxs[i]["values"] = input_devices
        if input_devices:
            self.device_comboboxs[i].current(0)

    def select_directory(self, i):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entries[i].delete(0, tk.END)
            self.dir_entries[i].insert(0, directory)

        self.set_directory(i, self.dir_entries[i].get())

    def set_directory(self, i, directory):

        if directory != "":
            self.selected_directories[i] = directory
            print("Directory ", i, " setted")

    def start(self, i):
        if not self.recording[i]:
            self.recording[i] = True
            print(f"Iniciando gravação para índice {i}")

            self.sd_inputs[i] = SDInput(device=self.selected_input_devices[i])
            self.sd_recorders[i] = SFRecorder(
                sd_input=self.sd_inputs[i],
                directory=self.selected_directories[i],
                daemon=True,
            )
            self.vus[i].set_player(self.sd_inputs[i])
            self.sd_recorders[i].start()
            self.sd_recorders[i].start_record()

            self.start_buttons[i].configure(text="Gravando...", bg="red")

    def stop(self, i):
        if self.recording[i]:
            self.sd_inputs[i].stop()
            self.sd_recorders[i].stop_record()
            self.sd_recorders[i].set_running(False)
            self.recording[i] = False
            self.start_buttons[i].configure(text="Start", bg="SystemButtonFace")
        # self.vus[i].set_running(False)

    def on_close(self):
        # Pare todas as threads de gravação e VU
        for i in range(self.recorders):
            if i in self.sd_recorders:
                self.sd_recorders[i].stop_record()
                self.sd_recorders[i].set_running(False)
                # self.sd_recorders[i].join()
            if i in self.vus:
                self.vus[i].running = False
                # self.vus[i].join()

        self.master.destroy()
