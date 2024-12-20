from src.audio_processing import (
    load_audio,
    change_tempo,
    change_pitch,
    apply_reverb,
    apply_delay,
    export_audio,
)


def generate_remix(
    file_path,
    tempo_factor=1.0,
    pitch_steps=0,
    reverb_amount=0.0,
    delay_ms=0,
    feedback=0.0,
):

    audio, sr = load_audio(file_path)

    if tempo_factor != 1.0:
        audio = change_tempo(audio, tempo_factor)

    if pitch_steps != 0:
        audio = change_pitch(audio, sr, pitch_steps)

    if reverb_amount > 0.0:
        audio = apply_reverb(audio, sr, reverb_amount)

    if delay_ms > 0:
        audio = apply_delay(audio, sr, delay_ms, feedback)

    return audio, sr


def save_remix(audio, sr, output_path="export/remixed_track.wav"):
    export_audio(audio, sr, output_path)
    return output_path
