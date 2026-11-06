import numpy as np
import matplotlib.pyplot as plt


def plot_waveforms(original, quantized_signals, sample_rate):

    # Display first 20 milliseconds
    samples = int(sample_rate * 0.02)

    time = np.arange(samples) / sample_rate

    plt.figure(figsize=(12, 6))

    plt.plot(
        time,
        original[:samples],
        label="Original Audio",
        linewidth=2
    )

    for bits, signal in quantized_signals.items():

        plt.step(
            time,
            signal[:samples],
            where="mid",
            label=f"{bits}-bit PCM"
        )

    plt.title("PCM Quantization Comparison")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def plot_quantization_noise(original, quantized, sample_rate, bits):

    samples = int(sample_rate * 0.02)

    time = np.arange(samples) / sample_rate

    noise = original - quantized

    plt.figure(figsize=(12, 5))

    plt.plot(time, noise[:samples])

    plt.title(f"{bits}-bit Quantization Noise")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Noise Amplitude")
    plt.grid(True)

    plt.tight_layout()
    plt.show()