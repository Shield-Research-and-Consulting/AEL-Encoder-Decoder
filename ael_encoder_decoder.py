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

    # File & Communication Handling
    "FILE": 5100,
    "REPORT": 5200, # Report File
    "LOG": 5300,    # Log File
    "CONFIG": 5400, # Configuration File
    "MSG": 5500,    # Message
    "TEXT": 5600,   # Text File
    "BINARY": 5700, # Binary File

    # System States & Status Messages
    "STATE": 6000,
    "BUSY": 6100,   # System Busy
    "IDLE": 6200,   # System Idle
    "ERROR": 6300,  # System Error
    "SUCCESS": 6400,# Success Confirmation
    "WARNING": 6500, # Warning State

    "WEATHER": 7500, # Weather
    "BER": 8000,   # Berlin
    "TMR": 8500,   # Tomorrow
}

SAMPLE_RATE = 44100
DURATION = 0.3

# Encoder
def generate_tone(frequencies, duration=DURATION, sample_rate=SAMPLE_RATE):
    """Generates a combined sine wave for multiple frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += 0.5 * np.sin(2 * np.pi * freq * t)
    return wave / (len(frequencies) * 0.8)  # Reduces signal domination

def encode_ael_message(ael_command):
    """Encodes an AEL message into a frequency sequence."""
    print("Encoding Parts:", ael_command.split("|"))
    tones = []
    for part in ael_command.split("|"):
        freq = AEL_VOCAB.get(part, None)
        if freq:
            tones.append(generate_tone([freq]))
    return np.concatenate(tones)

def save_ael_message(ael_command, filename="ael_message.wav"):
    """Saves an AEL message as a WAV file."""
    audio_wave = encode_ael_message(ael_command)
    wav.write(filename, SAMPLE_RATE, (audio_wave * 32767).astype(np.int16))
    return filename

# Decoder
def detect_frequencies(audio_wave, sample_rate, n_fft=1024):
    """Performs a frequency analysis and extracts dominant frequencies."""
    f, t, Zxx = scipy.signal.stft(audio_wave, fs=sample_rate, nperseg=n_fft)
    detected_freqs = [int(round(f[np.argmax(np.abs(Zxx[:, i]))])) for i in range(Zxx.shape[1])]
    return detected_freqs

def adaptive_frequency_matching(detected_frequencies):
    """Matches detected frequencies to the closest known AEL vocabulary term."""
    reverse_map = {v: k for k, v in AEL_VOCAB.items()}
    matched_frequencies = []
    
    for freq in detected_frequencies:
        closest_freq = min(reverse_map.keys(), key=lambda f: abs(f - freq))
        tolerance = max(10, closest_freq * 0.01)  # Adjusted to 1% tolerance
        
        if abs(closest_freq - freq) <= tolerance:
            matched_frequencies.append(reverse_map[closest_freq])
        else:
            matched_frequencies.append("UNKNOWN")
    
    return matched_frequencies

def decode_ael_message(audio_file):
    """Decodes an AEL message from an audio file with duplicate filtering."""
    sample_rate, audio_wave = wav.read(audio_file)
    if len(audio_wave.shape) > 1:
        audio_wave = audio_wave[:, 0]

    detected_frequencies = detect_frequencies(audio_wave, sample_rate)
    decoded_commands = adaptive_frequency_matching(detected_frequencies)

    # **Filter out consecutive duplicate words**
    filtered_commands = [key for key, _ in groupby(decoded_commands)]
    
    return "|".join(filtered_commands)
