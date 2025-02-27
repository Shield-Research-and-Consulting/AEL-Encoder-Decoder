import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ael_encoder_decoder import decode_ael_message, detect_frequencies
import scipy.io.wavfile as wav

# Load audio file
sample_rate, audio_wave = wav.read("example_message.wav")

# Detect frequencies manually
detected_frequencies = detect_frequencies(audio_wave, sample_rate)

# print("Detected Frequencies:", detected_frequencies)

message = decode_ael_message("example_message.wav")
print("Dekodierte Nachricht:", message)