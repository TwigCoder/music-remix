import streamlit as st


def render_audio_preview(audio_file_path):
    if audio_file_path:
        st.subheader("Remix Preview")
        st.audio(audio_file_path, format="audio/wav")

    else:
        st.warning("⚠️ No remix available for preview. Please generate a remix first.")
