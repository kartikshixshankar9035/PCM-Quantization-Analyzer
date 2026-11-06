from src.audio_loader import load_audio
from src.quantizer import quantize_signal
from src.visualization import plot_waveforms, plot_quantization_noise

audio, sr = load_audio("data/audio/test_audio.wav")

q4 = quantize_signal(audio, 4)
q8 = quantize_signal(audio, 8)
q16 = quantize_signal(audio, 16)

signals = {
    4: q4,
    8: q8,
    16: q16
}

plot_waveforms(audio, signals, sr)

plot_quantization_noise(audio, q4, sr, 4)