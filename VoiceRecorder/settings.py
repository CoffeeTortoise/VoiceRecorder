from pyaudio import paInt16


# Recorder settings
CHUNK: int = 1_024
CHANNELS: int = 1
RATE: int = 44_100
FORMAT: int = paInt16
OUT_FORMATS: tuple[str, ...] = 'wav', 'ogg', 'mp3'
