import soundfile as sf
import numpy as np

def load_audio(file_path):

    audio, sample_rate = sf.read(file_path)

    # Convert stereo audio into mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Normalize audio
    audio = audio / np.max(np.abs(audio))

    duration = len(audio) / sample_rate

    print("Audio Loaded Successfully!")
    print("Sample Rate:", sample_rate, "Hz")
    print("Duration:", round(duration, 2), "seconds")
    print("Number of Samples:", len(audio))

    return audio, sample_rate