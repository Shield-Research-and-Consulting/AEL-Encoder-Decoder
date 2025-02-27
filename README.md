# AEL Encoder & Decoder

## 📌 Projektbeschreibung
Dieses Projekt enthält eine Implementierung eines **AEL (Artificial Encoded Language) Encoder & Decoder** für akustische Signalübertragung. Es ermöglicht die Kodierung von Nachrichten in **modulierte Tonfrequenzen** und deren anschließende **Dekodierung**.

## 🚀 Funktionen
- **Kodierung von AEL-Nachrichten** in Audiosignale (WAV-Format)
- **Dekodierung** von AEL-Tonsequenzen zurück in Text
- **Universelles Vokabular** für verschiedene Anwendungen (Steuerung, Sensorik, Security, Finanzen, AI, Kommunikation)
- **Adaptive Frequenz-Toleranz** zur Fehlerreduktion bei der Dekodierung
- **Redundanz-Filterung** für optimierte Signalinterpretation

## 📂 Projektstruktur
```
├── ael_encoder_decoder.py  # Hauptmodul für Encoder & Decoder
├── README.md               # Diese Datei mit Projektbeschreibung
├── requirements.txt        # Benötigte Python-Bibliotheken
├── examples/               # Beispiel-WAV-Dateien und Test-Skripte
│   ├── example_message.wav # Beispieldatei für einen kodierten AEL-String
│   ├── test_encoder.py     # Test für den Encoder
│   ├── test_decoder.py     # Test für den Decoder
├── utils/                  # Hilfsfunktionen für zukünftige Erweiterungen
│   ├── audio_tools.py      # Werkzeuge für Audioverarbeitung
│   ├── frequency_tools.py  # Werkzeuge für Frequenzanalyse
└── .gitignore              # Dateien und Verzeichnisse, die nicht getrackt werden sollen
```

## 📥 Installation
```sh
pip install -r requirements.txt
```

## 🔧 Nutzung
### **1. AEL-Nachricht kodieren & als Audio speichern**
```python
from ael_encoder_decoder import save_ael_message
save_ael_message("REQ|WEATHER|BER|TMR", "message.wav")
```

### **2. AEL-Nachricht aus einer Audiodatei dekodieren**
```python
from ael_encoder_decoder import decode_ael_message
message = decode_ael_message("message.wav")
print(message)
```

## 🎯 Anwendungsfälle
✅ **IoT & Sensordaten** (z. B. Temperaturübertragung mit `SENSOR|TEMP|22C`)

✅ **Sicherheit & Authentifizierung** (`SEC|AUTH|ACCESS` für Zugangskontrolle)

✅ **KI & Automatisierung** (`AI|TASK|PREDICT` für Machine Learning Modelle)

✅ **Finanztransaktionen** (`PAY|CRYPTO|BTC` für Blockchain-Zahlungen)


## 🔄 Erweiterbarkeit
- **Neues Vokabular hinzufügen**: Anpassung des `AEL_VOCAB`-Dictionaries
- **Andere Modulationsverfahren testen**: Erweiterung der Frequenzlogik

## 📌 Lizenz
MIT License - Open Source & für die Community 🌍
