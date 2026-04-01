import speech_recognition as sr
import time


def speech_to_text(file_path):
    """
    Converts audio to text using Google's Speech Engine with noise reduction.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            # Reduce ambient noise from the recording
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Try transcription with 2 retries
        for attempt in range(2):
            try:
                text = recognizer.recognize_google(audio_data)
                if text: return text
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                time.sleep(1)
                continue

        return "[No audible speech detected in the recording]"

    except Exception as e:
        return f"Transcription Error: {str(e)}"