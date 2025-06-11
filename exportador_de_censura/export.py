import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
from exportador import export_audio

caminho_perfis = "./../config.json"


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


class ExportadorGUI:
    def __init__(self, master, config):

        self.master = master
        self.config = config
        master.title("Exportador de Censura")

        # Perfis
        tk.Label(master, text="Perfil:").grid(row=0, column=0, sticky="e")
        self.perfil_combobox = ttk.Combobox(master, state="readonly", width=30)
        self.perfil_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_perfis()

        # Data/hora inicial
        tk.Label(master, text="Data Inicial:").grid(row=1, column=0, sticky="e")
        self.start_date = DateEntry(master, width=12, date_pattern="yyyy-mm-dd")
        self.start_date.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.start_time = ttk.Combobox(master, width=8, values=self.generate_times())
        self.start_time.set("00:00:00")
        self.start_time.grid(row=1, column=1, sticky="e", padx=5, pady=5)

        # Data/hora final
        tk.Label(master, text="Data Final:").grid(row=2, column=0, sticky="e")
        self.end_date = DateEntry(master, width=12, date_pattern="yyyy-mm-dd")
        self.end_date.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.end_time = ttk.Combobox(master, width=8, values=self.generate_times())
        self.end_time.set("23:59:59")
        self.end_time.grid(row=2, column=1, sticky="e", padx=5, pady=5)

        # Botão Exportar
        self.export_button = tk.Button(master, text="Exportar", command=self.exportar)
        self.export_button.grid(row=3, column=0, columnspan=2, pady=10)

    def generate_times(self):
        # Gera horários de 00:00:00 até 23:59:00 de minuto em minuto
        return [f"{h:02d}:{m:02d}:00" for h in range(24) for m in range(0, 60, 1)]

    def load_perfis(self):

        self.perfil_combobox["values"] = [
            c["nome"] for c in config["recorders_configs"]
        ]

    def get_perfil_by_name(self, name):

        for c in config["recorders_configs"]:
            if c["nome"] == name:
                return c

        return None

    def exportar(self):
        perfil = self.perfil_combobox.get()
        if not perfil:
            messagebox.showwarning("Atenção", "Selecione um perfil.")
            return
        try:
            base_dir = self.get_perfil_by_name(perfil)["caminho"]
        except:
            print("Erro ao carregar perfil")

        start_time = f"{self.start_date.get()} {self.start_time.get()}"
        end_time = f"{self.end_date.get()} {self.end_time.get()}"

        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav", filetypes=[("WAV", "*.wav"), ("MP3", "*.mp3")]
        )
        if not output_path:
            return
        try:
            export_audio(base_dir, start_time, end_time, output_path)
            messagebox.showinfo("Sucesso", f"Exportação concluída: {output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")


if __name__ == "__main__":

    import checker

    if not checker.check():
        root = tk.Tk()
        root.geometry("300x200")
        label = tk.Label(root, text="Infelizmente seu produto expirou")
        label.pack(anchor=tk.CENTER)
        root.mainloop()
        exit()

    config_path = ask_config_path()
    if not config_path:
        exit()  # Usuário cancelou

    config = load_config(config_path)
    if not config:
        exit()  # Erro ao carregar

    root = tk.Tk()
    app = ExportadorGUI(root, config)
    root.mainloop()
