from media_devices.player_sounddevice import SDInput
from recorder.sfrecorder import SFRecorder
from window import MainWindow
import tkinter as tk
from tkinter import filedialog, messagebox
from web.web_app import app
import threading
import json


# recorder.record()
def start_flask():
    app.run(debug=True, use_reloader=False)


def ask_config_path():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    config_path = filedialog.askopenfilename(
        title="Selecione o arquivo config.json", filetypes=[("JSON files", "*.json")]
    )
    root.destroy()
    return config_path


def load_config(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao carregar config.json:\n{e}")
        return None


def run():

    import checker

    if not checker.check():
        root = tk.Tk()
        root.geometry("300x200")
        label = tk.Label(root, text="Infelizmente seu produto expirou")
        label.pack()
        root.mainloop()
        exit()

    config_path = ask_config_path()
    if not config_path:
        exit()  # Usuário cancelou

    config = load_config(config_path)
    if not config:
        exit()  # Erro ao carregar

    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    root = tk.Tk()
    app = MainWindow(root, config=config)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    run()
