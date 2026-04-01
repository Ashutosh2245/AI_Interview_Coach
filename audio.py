import librosa
import numpy as np


def analyze_audio(file_path):
    """
    Extracts RMS Energy and Zero Crossing Rate for speech analysis.
    """
    try:
        y, sr = librosa.load(file_path)

        # 1. Energy (Loudness)
        rms = librosa.feature.rms(y=y)
        avg_energy = np.mean(rms)

        # 2. Pitch/Frequency stability
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_score = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0

        # 3. Silence Detection (Tempo)
        intervals = librosa.effects.split(y, top_db=20)
        speech_ratio = sum([i[1] - i[0] for i in intervals]) / len(y)

        # Normalized metrics
        metrics = {
            "energy": float(avg_energy),
            "clarity": float(speech_ratio),
            "pitch_stability": float(pitch_score)
        }

        return metrics
    except Exception as e:
        return {"energy": 0.0, "clarity": 0.0, "pitch_stability": 0.0}