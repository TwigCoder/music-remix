from src.file_manager import save_uploaded_file, get_export_file_path
from src.remix_engine import generate_remix, save_remix
import streamlit as st


def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file)
        st.success("File uploaded successfully!")
        return file_path
    else:
        st.error("⚠️ Please upload a valid audio file.")
        return None


def handle_remix_generation(file_path, remix_settings):
    if not file_path:
        st.error("⚠️ Please upload a file before generating a remix.")
        return None

    with st.spinner("Generating remix... Please wait."):
        remixed_audio, sr = generate_remix(
            file_path,
            tempo_factor=remix_settings["tempo_factor"],
            pitch_steps=remix_settings["pitch_steps"],
            reverb_amount=remix_settings["reverb_amount"],
            delay_ms=remix_settings["delay_ms"],
            feedback=remix_settings["feedback"],
        )

        export_file_path = get_export_file_path()
        save_remix(remixed_audio, sr, export_file_path)

        st.success("Remix generated successfully!")
        return export_file_path
