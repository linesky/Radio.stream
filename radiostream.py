
import pyaudio
import socketio
import threading
from flask import Flask, render_template
#pip install pyaudio flask flask-socketio
# Configurações de áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Configurações do Flask
app = Flask(__name__)
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@app.route('/')
def index():
    return render_template('index.html')

# Função para capturar e enviar áudio
def audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Transmitting audio... Press Ctrl+C to stop.")
    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            sio.emit('audio', data)
    except KeyboardInterrupt:
        pass

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Transmission stopped.")

# SocketIO evento para conectar
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

# SocketIO evento para desconectar
@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# Iniciar a transmissão de áudio em uma thread separada
audio_thread = threading.Thread(target=audio_stream)
audio_thread.start()

# Iniciar a aplicação Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
