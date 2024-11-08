from pyaudio import PyAudio
import wave
from settings import*
from config import OUT_FOLDER
from timer import Timer


class SoundRecorder:
    def __init__(self) -> None:
        self.filename: str = 'example'
        self.time_lim: int = 1
        self.out: int = 0
        self.audio: list[int] = []
        
    def record(self) -> PyAudio:
        recorder: PyAudio = PyAudio()
        stream = recorder.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)
        timer: Timer = Timer()
        recording: bool = True
        while recording:
            data: int = stream.read(CHUNK)
            self.audio.append(data)
            time: float = timer.get_time()
            if time >= self.time_lim:
                recording = False
        stream.stop_stream()
        stream.close()
        return recorder
    
    def save(self, recorder: PyAudio) -> None:
        out_file: str = f'{OUT_FOLDER}/{self.filename}.{OUT_FORMATS[self.out]}'
        with wave.open(out_file, 'wb') as file:
            file.setnchannels(CHANNELS)
            file.setsampwidth(recorder.get_sample_size(FORMAT))
            file.setframerate(RATE)
            file.writeframes(b''.join(self.audio))
        recorder.terminate()


if __name__ == '__main__':
    rec: SoundRecorder = SoundRecorder()
    recorder: PyAudio = rec.record()
    rec.save(recorder)
