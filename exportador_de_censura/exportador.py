import os
import soundfile as sf
from datetime import datetime, timedelta
import numpy as np
import re


def list_files_in_range(base_dir, start_dt, end_dt):
    files = []
    # Percorre todas as pastas de data/hora entre start_dt e end_dt
    current = start_dt.replace(minute=0, second=0, microsecond=0)
    end_limit = end_dt + timedelta(hours=1)
    while current <= end_limit:
        date_folder = current.strftime("%Y%m%d")
        hour_folder = current.strftime("%H")
        folder_path = os.path.join(base_dir, date_folder, hour_folder)
        if os.path.isdir(folder_path):
            for fname in os.listdir(folder_path):
                # Espera padrão: YYYYMMDDHHMMSS-gravacao.mp3
                match = re.match(r"(\d{14})-gravacao\.mp3$", fname)
                if match:
                    file_dt = datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
                    file_path = os.path.join(folder_path, fname)
                    # Considera arquivos que tocam qualquer parte do intervalo
                    if file_dt >= start_dt and file_dt - timedelta(seconds=10) < end_dt:
                        files.append((file_path, file_dt))
        current += timedelta(hours=1)
    # Ordena por data/hora
    files.sort(key=lambda x: x[1])
    return files


def export_audio(base_dir, start_time, end_time, output_path):
    # start_time e end_time são strings no formato 'YYYY-MM-DD HH:MM:SS'
    start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    files = list_files_in_range(base_dir, start_dt, end_dt)
    audio_data = []
    samplerate = None

    for file_path, file_dt in files:
        data, sr = sf.read(file_path)
        if samplerate is None:
            samplerate = sr
        # Calcula o offset de início e fim para o primeiro e último arquivo
        file_start = file_dt - timedelta(seconds=10)
        file_end = file_dt
        seg_start = max((start_dt - file_start).total_seconds(), 0)
        seg_end = min((end_dt - file_start).total_seconds(), 10)
        start_sample = int(seg_start * sr)
        end_sample = int(seg_end * sr)
        audio_data.append(data[start_sample:end_sample])

    if audio_data:
        output = audio_data[0]
        for part in audio_data[1:]:
            output = np.concatenate((output, part))
        sf.write(output_path, output, samplerate)
        print(f"Exportado para {output_path}")
    else:
        print("Nenhum arquivo encontrado para o período informado.")


if __name__ == "__main__":
    # Exemplo de uso
    base_dir = r"C:\Users\kdtorres\Documents\Programacao\Band\gravador_de_censura\gravacoes\gravador3"
    start_time = "2025-06-10 16:00:00"
    end_time = "2025-06-10 16:05:00"
    output_path = "exportado.wav"
    export_audio(base_dir, start_time, end_time, output_path)
