import numpy as np
import scipy.io.wavfile as wav
import scipy.signal
from collections import Counter
from itertools import groupby

# Universal AEL Vocabulary
AEL_VOCAB = {
    # Core Commands
    "REQ": 1200,   # Request
    "ACT": 1300,   # Action
    "DATA": 1400,  # Data Transfer
    "CONF": 1500,  # Confirmation
    "ERR": 1600,   # Error

    # Sensor Data & Environmental Variables
    "SENSOR": 2000,
    "TEMP": 2100,  # Temperature
    "HUM": 2200,   # Humidity
    "PRESS": 2300, # Pressure
    "GPS": 2400,   # GPS Data
    "SPEED": 2500, # Speed
    "VOLT": 2600,  # Voltage
    "AMP": 2700,   # Amperage (Current)
    "STATE": 2800, # System State

    # Security & Access Control
    "SEC": 3000,
    "AUTH": 3100,  # Authentication
    "LOCK": 3200,  # Lock
    "UNLOCK": 3300, # Unlock
    "ACCESS": 3400, # Access Control
    "DENY": 3500,   # Access Denied

    # AI & Automation
    "AI": 3700,
    "TASK": 3800,   # Task Execution
    "LEARN": 3900,  # Machine Learning
    "PREDICT": 4000,# Prediction Model
    "REPLY": 4100,  # Auto-Reply
    "LOGIC": 4200,  # Logic Decision

    # Financial Transactions & Payments
    "PAY": 4500,
    "BILL": 4600,   # Billing
    "CRYPTO": 4700, # Cryptocurrency
    "FIAT": 4800,   # Fiat Currency
    "EXCH": 4900,   # Exchange Rate

    # System States & Status Messages
    "STATE": 5000,
    "BUSY": 5100,   # System Busy
    "IDLE": 5200,   # System Idle
    "ERROR": 5300,  # System Error
    "SUCCESS": 5400,# Success Confirmation
    "WARNING": 5500, # Warning State

    # Weather & Location Data
    "WEATHER": 5600, # Weather
    "BER": 5700,   # Berlin
    "TMR": 5800,   # Tomorrow
}

SAMPLE_RATE = 48000
DURATION = 0.5

# Encoder
def generate_tone(frequencies, duration=DURATION, sample_rate=SAMPLE_RATE):
    """Generates a combined sine wave for multiple frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += 0.5 * np.sin(2 * np.pi * freq * t)
    return wave / (len(frequencies) * 0.8)  # Reduces signal domination

def encode_ael_message(ael_command):
    """Encodes an AEL message into a frequency sequence with support for free text (CONTENT)."""
    tones = []
    silence = np.zeros(int(SAMPLE_RATE * 0.01))  # Short silence between tones
    for part in ael_command.split("|"):
        if part.startswith("CONTENT\"") and part.endswith("\""):
            text = part[8:-1]  # Extract the quoted text
            text_frequencies = []
            for char in text:
                freq = ord(char) * 10 + 7000
                print(f"ENCODER: '{char}' → {freq} Hz")  # Debugging-Ausgabe
                text_frequencies.append(freq)
                tones.append(generate_tone(text_frequencies))
                tones.append(silence) 
        else:
            freq = AEL_VOCAB.get(part, None)
            if freq:
                print(f"Befehl/ID '{part}' wird mit Frequenz {freq} Hz encodiert")  # Debugging-Ausgabe
                tones.append(generate_tone([freq]))
            else:
                print(f"Unbekannter Befehl/ID '{part}', kann nicht encodiert werden!")  # Fehlerhinweis
        tones.append(silence)  # Insert pause
    return np.concatenate(tones)

def save_ael_message(ael_command, filename="ael_message.wav"):
    """Saves an AEL message as a WAV file."""
    audio_wave = encode_ael_message(ael_command)
    wav.write(filename, SAMPLE_RATE, (audio_wave * 32767).astype(np.int16))
    return filename

# Decoder
def detect_frequencies(audio_wave, sample_rate, n_fft=1024):
    """Performs a frequency analysis and extracts dominant frequencies."""
    # f, t, Zxx = scipy.signal.stft(audio_wave, fs=sample_rate, nperseg=n_fft)
    f, t, Zxx = scipy.signal.stft(audio_wave, fs=sample_rate, nperseg=4096)
    detected_freqs = [int(round(f[np.argmax(np.abs(Zxx[:, i]))])) for i in range(Zxx.shape[1])]
    return detected_freqs

def adaptive_frequency_matching(detected_frequencies):
    """Matches detected frequencies to the closest known AEL vocabulary term or decodes free text."""
    reverse_map = {v: k for k, v in AEL_VOCAB.items()}
    matched_frequencies = []

    for freq in detected_frequencies:
        if freq <= 1200:
            continue  # Ignoriere Stille

        if 7000 <= freq < 10000:  # **ASCII-Freitextbereich**
            ascii_val = int(((freq + 5) - 7000) / 10)  # ASCII-Wert berechnen
            if 32 <= ascii_val <= 126:  # Nur druckbare Zeichen zulassen
                char = chr(ascii_val)
                print(f"Erkannter Freitext-Buchstabe '{char}' aus Frequenz {freq} Hz, ASCII {ascii_val}")  # Debugging-Ausgabe
            else:
                char = "?"  # Platzhalter für ungültige Zeichen
                print(f"Ungültige Frequenz {freq} Hz für ASCII, ersetzt durch '?'")
            matched_frequencies.append(f"CHAR_{char}")
        elif freq < 6000:  # **Nur Befehle unter 6000 Hz erlauben**
            closest_freq = min(reverse_map.keys(), key=lambda f: abs(f - freq))
            tolerance = max(30, closest_freq * 0.3)  # **Toleranz auf 3% erhöhen**

            if abs(closest_freq - freq) <= tolerance:
                print(f"Erkannter Befehl/ID '{reverse_map[closest_freq]}' aus Frequenz {freq} Hz")  # Debugging-Ausgabe
                matched_frequencies.append(reverse_map[closest_freq])
            else:
                print(f"Unbekannte Frequenz {freq} Hz, kein passender Befehl gefunden!")  # Fehlerhinweis
                matched_frequencies.append(f"UNKNOWN_{freq}")  # Debugging
        else:
            print(f"Unbekannte hohe Frequenz {freq} Hz, ignoriert.")  # Fehlerhinweis
            matched_frequencies.append(f"UNKNOWN_{freq}")  # Hohe Frequenzen ignorieren

    return matched_frequencies

def decode_ael_message(audio_file):
    """Decodes an AEL message from an audio file, supporting quoted CONTENT messages."""
    sample_rate, audio_wave = wav.read(audio_file)
    if len(audio_wave.shape) > 1:
        audio_wave = audio_wave[:, 0]

    detected_frequencies = detect_frequencies(audio_wave, sample_rate)
    decoded_commands = adaptive_frequency_matching(detected_frequencies)

    content_buffer = []
    final_message = []
    in_content = False

    for cmd in decoded_commands:
        if cmd.startswith("CHAR_"):  # Beginne Freitext
            if not in_content:
                in_content = True
                final_message.append("CONTENT\"")
            content_buffer.append(cmd.split("_")[1])  # Zeichen extrahieren
        else:
            if in_content:
                final_message.append("".join(content_buffer) + "\"")  # Satz schließen
                in_content = False
                content_buffer = []
            final_message.append(cmd)

    if in_content:
        final_message.append("".join(content_buffer) + "\"")

    return "|".join([key for key, _ in groupby(final_message)])  # Gruppiere doppelte Einträge









