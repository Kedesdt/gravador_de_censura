import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
import json
from datetime import datetime
from exportador import export_audio

caminho_perfis = "./../config.json"


class ExportadorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Exportador de Censura")

        # Perfis
        tk.Label(master, text="Perfil:").grid(row=0, column=0, sticky="e")
        self.perfil_combobox = ttk.Combobox(master, state="readonly", width=30)
        self.perfil_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_perfis()

        # Data/hora inicial
        tk.Label(master, text="Data/Hora Inicial (YYYY-MM-DD HH:MM:SS):").grid(
            row=1, column=0, sticky="e"
        )
        self.start_entry = tk.Entry(master, width=25)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)

        # Data/hora final
        tk.Label(master, text="Data/Hora Final (YYYY-MM-DD HH:MM:SS):").grid(
            row=2, column=0, sticky="e"
        )
        self.end_entry = tk.Entry(master, width=25)
        self.end_entry.grid(row=2, column=1, padx=5, pady=5)

        # Botão Exportar
        self.export_button = tk.Button(master, text="Exportar", command=self.exportar)
        self.export_button.grid(row=3, column=0, columnspan=2, pady=10)

    def load_perfis(self):
        try:
            with open(caminho_perfis, "r", encoding="utf-8") as f:
                self.perfis = json.load(f)
            self.perfil_combobox["values"] = list(self.perfis.keys())
            if self.perfis:
                self.perfil_combobox.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar perfis: {e}")
            self.perfis = {}

    def exportar(self):
        perfil = self.perfil_combobox.get()
        if not perfil:
            messagebox.showwarning("Atenção", "Selecione um perfil.")
            return
        base_dir = self.perfis[perfil]["base_dir"]
        start_time = self.start_entry.get()
        end_time = self.end_entry.get()
        try:
            # Valida datas
            datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        except Exception:
            messagebox.showerror("Erro", "Datas em formato inválido.")
            return
        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav", filetypes=[("WAV", "*.wav")]
        )
        if not output_path:
            return
        try:
            export_audio(base_dir, start_time, end_time, output_path)
            messagebox.showinfo("Sucesso", f"Exportação concluída: {output_path}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExportadorGUI(root)
    root.mainloop()
