import librosa
import numpy as np
from pydub import AudioSegment
import soundfile as sf


def load_audio(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    return audio, sr


def change_tempo(audio, factor):
    return librosa.effects.time_stretch(audio, rate=factor)


def change_pitch(audio, sr, steps):
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=steps)


def apply_reverb(audio, sr, reverb_amount=0.5):
    wet = librosa.effects.preemphasis(audio, coef=reverb_amount)
    return wet


def apply_delay(audio, sr, delay_ms=500, feedback=0.5):
    delay_samples = int(sr * delay_ms / 1000)
    delayed = np.pad(audio, (delay_samples, 0))
    mix = (audio + feedback * delayed[: len(audio)]) / (1 + feedback)
    return mix


def export_audio(audio, sr, output_path, format="wav"):
    sf.write(output_path, audio, sr, format=format)


def analyze_audio(file_path):
    audio, sr = load_audio(file_path)
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
    key = librosa.key.key(audio, sr=sr)
    duration = librosa.get_duration(y=audio, sr=sr)
    return {"tempo": tempo, "key": key, "duration": duration}


def convert_to_wav(file_path):
    audio = AudioSegment.from_file(file_path)
    output_path = file_path.rsplit(".", 1)[0] + ".wav"
    audio.export(output_path, format="wav")
    return output_path
