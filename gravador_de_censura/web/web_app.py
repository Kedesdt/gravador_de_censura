from flask import Flask, render_template_string, request, jsonify
import sounddevice as sd
import threading
import os

app = Flask(__name__)

# Variáveis globais para simular o estado
recording = False
selected_device = None
selected_directory = os.getcwd()


@app.route("/")
def index():
    devices = [d["name"] for d in sd.query_devices() if d["max_input_channels"] > 0]
    return render_template_string(
        """
        <h2>Gravador de Censura (Web)</h2>
        <form method="post" action="/set_directory">
            Diretório: <input name="directory" value="{{directory}}" size="40">
            <button type="submit">Selecionar</button>
        </form>
        <form method="post" action="/set_device">
            Device de Áudio:
            <select name="device">
                {% for d in devices %}
                <option value="{{d}}" {% if d==device %}selected{% endif %}>{{d}}</option>
                {% endfor %}
            </select>
            <button type="submit">Selecionar</button>
        </form>
        <form method="post" action="/start">
            <button type="submit" {% if recording %}disabled{% endif %}>Start</button>
        </form>
        <form method="post" action="/stop">
            <button type="submit" {% if not recording %}disabled{% endif %}>Stop</button>
        </form>
        <p>Status: {{'Gravando...' if recording else 'Parado'}}</p>
        <!-- Aqui você pode adicionar um canvas ou SVG para o VU meter futuramente -->
    """,
        devices=devices,
        device=selected_device,
        directory=selected_directory,
        recording=recording,
    )


@app.route("/set_directory", methods=["POST"])
def set_directory():
    global selected_directory
    selected_directory = request.form["directory"]
    return index()


@app.route("/set_device", methods=["POST"])
def set_device():
    global selected_device
    selected_device = request.form["device"]
    return index()


@app.route("/start", methods=["POST"])
def start():
    global recording
    recording = True
    # Aqui você pode iniciar a thread de gravação real
    return index()


@app.route("/stop", methods=["POST"])
def stop():
    global recording
    recording = False
    # Aqui você pode parar a thread de gravação real
    return index()


if __name__ == "__main__":
    app.run(debug=True)
