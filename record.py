import sounddevice as sd
from scipy.io.wavfile import write
import uuid
import os
import streamlit as st


def record_audio(duration=30, fs=44100):
    """
    Records audio with a unique filename and error handling.
    """
    unique_id = uuid.uuid4().hex[:8]
    filename = f"interview_audio_{unique_id}.wav"

    try:
        st.info(f"🎤 Recording in progress for {duration} seconds...")

        # Audio device validation
        devices = sd.query_devices()
        if not devices:
            st.error("No Microphone found!")
            return None

        # Start recording
        recording = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype='int16'
        )

        # We don't use sd.wait() directly to allow UI responsiveness
        # But for simplicity in this flow, we wait for the buffer to fill
        sd.wait()

        write(filename, fs, recording)

        if os.path.exists(filename) and os.path.getsize(filename) > 1000:
            return filename
        else:
            return None

    except Exception as e:
        st.error(f"Recording Error: {str(e)}")
        return None


def cleanup_audio(filename):
    if filename and os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            pass