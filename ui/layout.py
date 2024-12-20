import streamlit as st
import librosa
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

hop_length = 2048


def render_sidebar():
    st.sidebar.header("Remix Settings")
    tempo_factor = st.sidebar.slider("Tempo Change (x)", 0.5, 2.0, 1.0, 0.1)
    pitch_steps = st.sidebar.slider("Pitch Shift (semitones)", -12, 12, 0, 1)
    reverb_amount = st.sidebar.slider("Reverb Amount", 0.0, 1.0, 0.0, 0.1)
    delay_ms = st.sidebar.slider("Delay (ms)", 0, 1000, 0, 50)
    feedback = st.sidebar.slider("Delay Feedback", 0.0, 1.0, 0.0, 0.1)
    return {
        "tempo_factor": tempo_factor,
        "pitch_steps": pitch_steps,
        "reverb_amount": reverb_amount,
        "delay_ms": delay_ms,
        "feedback": feedback,
    }


def render_main_interface():
    st.title("Music Remix Tool")
    uploaded_file = st.file_uploader("Upload MP3 or WAV", type=["mp3", "wav"])
    remix_button = st.button("Generate Remix")
    return uploaded_file, remix_button


def plot_waveform(original_audio, remixed_audio, sr):
    rms_orig = librosa.feature.rms(y=original_audio, hop_length=hop_length)[0]
    rms_remix = librosa.feature.rms(y=remixed_audio, hop_length=hop_length)[0]
    times = librosa.times_like(rms_orig, sr=sr, hop_length=hop_length)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times, y=rms_orig, name="Original"))
    fig.add_trace(go.Scatter(x=times, y=rms_remix, name="Remixed"))
    fig.update_layout(height=300, title="Amplitude Envelope")
    st.plotly_chart(fig, use_container_width=True)


def plot_spectrogram(original_audio, remixed_audio, sr):
    n_mels = 32

    mel_orig = librosa.feature.melspectrogram(
        y=original_audio, sr=sr, n_mels=n_mels, hop_length=hop_length
    )
    mel_remix = librosa.feature.melspectrogram(
        y=remixed_audio, sr=sr, n_mels=n_mels, hop_length=hop_length
    )

    mel_orig_db = librosa.power_to_db(mel_orig, ref=np.max)
    mel_remix_db = librosa.power_to_db(mel_remix, ref=np.max)

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Original", "Remixed"))
    fig.add_trace(go.Heatmap(z=mel_orig_db, colorscale="Viridis"), row=1, col=1)
    fig.add_trace(go.Heatmap(z=mel_remix_db, colorscale="Viridis"), row=2, col=1)
    fig.update_layout(height=400, title="Mel Spectrogram")
    st.plotly_chart(fig, use_container_width=True)


def plot_pitch(original_audio, remixed_audio, sr):
    pitches_orig, magnitudes_orig = librosa.piptrack(
        y=original_audio, sr=sr, hop_length=hop_length
    )
    pitches_remix, magnitudes_remix = librosa.piptrack(
        y=remixed_audio, sr=sr, hop_length=hop_length
    )

    pitch_orig = np.mean(pitches_orig, axis=0)[:50]
    pitch_remix = np.mean(pitches_remix, axis=0)[:50]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=pitch_orig, name="Original"))
    fig.add_trace(go.Scatter(y=pitch_remix, name="Remixed"))
    fig.update_layout(height=300, title="Average Pitch")
    st.plotly_chart(fig, use_container_width=True)


def plot_energy_bands(original_audio, remixed_audio, sr):
    n_bands = 6
    bands_orig = librosa.feature.mfcc(y=original_audio, sr=sr, n_mfcc=n_bands)
    bands_remix = librosa.feature.mfcc(y=remixed_audio, sr=sr, n_mfcc=n_bands)

    bands_orig_mean = np.mean(bands_orig, axis=1)
    bands_remix_mean = np.mean(bands_remix, axis=1)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(range(n_bands)), y=bands_orig_mean, name="Original"))
    fig.add_trace(go.Bar(x=list(range(n_bands)), y=bands_remix_mean, name="Remixed"))
    fig.update_layout(height=300, title="Frequency Band Energy")
    st.plotly_chart(fig, use_container_width=True)


def plot_tempo_comparison(original_audio, remixed_audio, sr):
    hop_length = 2048
    onset_env_orig = librosa.onset.onset_strength(
        y=original_audio, sr=sr, hop_length=hop_length
    )
    onset_env_remix = librosa.onset.onset_strength(
        y=remixed_audio, sr=sr, hop_length=hop_length
    )

    onset_orig = onset_env_orig[:50]
    onset_remix = onset_env_remix[:50]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=onset_orig, name="Original"))
    fig.add_trace(go.Scatter(y=onset_remix, name="Remixed"))
    fig.update_layout(height=300, title="Onset Strength")
    st.plotly_chart(fig, use_container_width=True)
