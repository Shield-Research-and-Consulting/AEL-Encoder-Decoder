import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ael_encoder_decoder import save_ael_message
save_ael_message("REQ|WEATHER|BER|TMR", "example_message.wav")
print("Test-Encoder erfolgreich.")