import os
import soundfile as sf
import time


def save(path, data, samplerate):
    # Obtém data e hora atuais
    now = time.localtime()
    date_folder = time.strftime("%Y%m%d", now)
    hour_folder = time.strftime("%H", now)

    # Acrescenta YYYYMMDD/HH ao caminho
    directory, filename = os.path.split(path)
    new_directory = os.path.join(directory, date_folder, hour_folder)
    if new_directory and not os.path.exists(new_directory):
        os.makedirs(new_directory, exist_ok=True)

    new_path = os.path.join(new_directory, filename)
    sf.write(new_path, data, samplerate=samplerate)
