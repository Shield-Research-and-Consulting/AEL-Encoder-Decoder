import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
from collections import Counter

# Universelles AEL-Vokabular
AEL_VOCAB = {
    "REQ": 1200, "ACT": 1300, "DATA": 1500, "CONF": 1800, "ERR": 2100,
    "SENSOR": 1400, "TEMP": 1450, "HUM": 1550, "PRESS": 1600, "GPS": 1650,
    "SEC": 1700, "AUTH": 1750, "LOCK": 1800, "UNLOCK": 1850, "ACCESS": 1900,
    "AI": 1950, "TASK": 2000, "LEARN": 2050, "PREDICT": 2100, "REPLY": 2150,
    "PAY": 2200, "BILL": 2250, "CRYPTO": 2300, "FIAT": 2350, "EXCH": 2400
}

SAMPLE_RATE = 44100
DURATION = 0.1

# Encoder
def generate_tone(frequencies, duration=DURATION, sample_rate=SAMPLE_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += 0.5 * np.sin(2 * np.pi * freq * t)
    return wave / len(frequencies)

def encode_ael_message(ael_command):
    tones = []
    for part in ael_command.split("|"):
        freq = AEL_VOCAB.get(part, None)
        if freq:
            tones.append(generate_tone([freq]))
    return np.concatenate(tones)

def save_ael_message(ael_command, filename="ael_message.wav"):
    audio_wave = encode_ael_message(ael_command)
    wav.write(filename, SAMPLE_RATE, (audio_wave * 32767).astype(np.int16))
    return filename

# Decoder
def detect_frequencies(audio_wave, sample_rate, n_fft=1024):
    f, t, Zxx = scipy.signal.stft(audio_wave, fs=sample_rate, nperseg=n_fft)
    detected_freqs = [int(round(f[np.argmax(np.abs(Zxx[:, i]))])) for i in range(Zxx.shape[1])]
    return detected_freqs

def decode_ael_message(audio_file):
    sample_rate, audio_wave = wav.read(audio_file)
    if len(audio_wave.shape) > 1:
        audio_wave = audio_wave[:, 0]
    detected_frequencies = detect_frequencies(audio_wave, sample_rate)
    reverse_map = {v: k for k, v in AEL_VOCAB.items()}
    return "|".join([reverse_map.get(freq, "UNKNOWN") for freq in detected_frequencies])
