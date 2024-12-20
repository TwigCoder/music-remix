import streamlit as st
import librosa
from ui.layout import (
    render_sidebar,
    render_main_interface,
    plot_waveform,
    plot_spectrogram,
    plot_pitch,
    plot_energy_bands,
    plot_tempo_comparison,
)
from ui.controls import handle_file_upload, handle_remix_generation
from src.file_manager import clear_directory

clear_directory("uploads")
clear_directory("export")


def main():
    st.set_page_config(page_title="Music Remix Tool", layout="wide")

    remix_settings = render_sidebar()
    uploaded_file, remix_button = render_main_interface()

    file_path = handle_file_upload(uploaded_file)

    if remix_button and file_path:
        export_file_path = handle_remix_generation(file_path, remix_settings)

        if export_file_path:
            original_audio, sr = librosa.load(file_path, sr=22050, duration=30)
            remixed_audio, _ = librosa.load(export_file_path, sr=22050, duration=30)

            st.audio(export_file_path, format="audio/wav")

            col1, col2 = st.columns(2)

            with col1:
                plot_waveform(original_audio, remixed_audio, sr)
                plot_pitch(original_audio, remixed_audio, sr)
                plot_energy_bands(original_audio, remixed_audio, sr)

        with col2:
            plot_spectrogram(original_audio, remixed_audio, sr)
            plot_tempo_comparison(original_audio, remixed_audio, sr)


if __name__ == "__main__":
    main()
