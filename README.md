# AEL Encoder & Decoder

## 📌 Project Description
This project implements an **AEL (Artificial Encoded Language) Encoder & Decoder** for acoustic signal transmission. It enables encoding messages into **modulated sound frequencies** and subsequently **decoding** them.

### Author Information:

- Stefan Tannhäuser, st@shield-research-consulting.de

## 🚀 Features
- **Encodes AEL messages** into audio signals (WAV format)
- **Decodes** AEL tone sequences back into text
- **Universal vocabulary** for various applications (Control, Sensors, Security, Finance, AI, Communication)
- **Adaptive frequency tolerance** to reduce decoding errors
- **Redundancy filtering** for optimized signal interpretation

## 📂 Project Structure
```
├── ael_encoder_decoder.py  # Main module for Encoder & Decoder
├── README.md               # This file with project documentation
├── requirements.txt        # Required Python libraries
├── examples/               # Example WAV files and test scripts
│   ├── example_message.wav # Sample file for an encoded AEL string
│   ├── test_encoder.py     # Test for the encoder
│   ├── test_decoder.py     # Test for the decoder
├── utils/                  # Utility functions for future expansions
│   ├── audio_tools.py      # Tools for audio processing
│   ├── frequency_tools.py  # Tools for frequency analysis
└── .gitignore              # Files and directories to be ignored by Git
```

## 📥 Installation
```sh
pip install -r requirements.txt
```

## 🔧 Usage
### **1. Encode an AEL message & save it as an audio file**
```python
from ael_encoder_decoder import save_ael_message
save_ael_message("REQ|WEATHER|BER|TMR", "message.wav")
```

### **2. Decode an AEL message from an audio file**
```python
from ael_encoder_decoder import decode_ael_message
message = decode_ael_message("message.wav")
print(message)
```

## 🎯 Use Cases
✅ **IoT & Sensor Data** (e.g., transmitting temperature with `SENSOR|TEMP|22C`)
✅ **Security & Authentication** (`SEC|AUTH|ACCESS` for access control)
✅ **AI & Automation** (`AI|TASK|PREDICT` for machine learning models)
✅ **Financial Transactions** (`PAY|CRYPTO|BTC` for blockchain payments)

## 🔄 Expandability
- **Add new vocabulary**: Modify the `AEL_VOCAB` dictionary
- **Experiment with different modulation methods**: Extend the frequency logic

## 📌 License
MIT License - Open Source & for the community 🌍

