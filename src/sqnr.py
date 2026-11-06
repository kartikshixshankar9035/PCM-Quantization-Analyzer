import numpy as np


def calculate_sqnr(original, quantized):

    # Calculate quantization noise
    noise = original - quantized

    # Calculate signal power
    signal_power = np.mean(original ** 2)

    # Calculate noise power
    noise_power = np.mean(noise ** 2)

    # Avoid division by zero
    if noise_power == 0:
        return float("inf")

    # Calculate SQNR in decibels
    sqnr = 10 * np.log10(signal_power / noise_power)

    return sqnr