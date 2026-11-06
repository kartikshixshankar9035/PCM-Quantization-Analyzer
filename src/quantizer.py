import numpy as np


def quantize_signal(signal, bits):
    """
    Quantize an audio signal using uniform PCM quantization.

    Parameters:
        signal: Input audio signal
        bits: Quantization bit depth (4, 8, or 16)

    Returns:
        Quantized audio signal
    """

    if bits not in [4, 8, 16]:
        raise ValueError("Supported bit depths are 4, 8, and 16.")

    # Number of quantization levels
    levels = 2 ** bits

    # Quantization step size
    step_size = 2.0 / (levels - 1)

    # Clip signal to the range [-1, 1]
    signal = np.clip(signal, -1.0, 1.0)

    # Perform uniform quantization
    quantized = np.round((signal + 1.0) / step_size)

    # Convert quantized values back to audio amplitude
    quantized = quantized * step_size - 1.0

    return quantized