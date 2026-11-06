# PCM Quantization and Noise Analyzer

A Python-based application that demonstrates how Pulse Code Modulation (PCM) quantization affects digital audio quality at different bit depths.

## Project Overview

This project analyzes the effect of quantization on audio signals by comparing original and quantized audio.

It calculates Signal-to-Quantization-Noise Ratio (SQNR) and visualizes how quantization bit depth affects audio quality.

## Features

- Upload WAV audio files.
- Display audio information.
- Perform PCM quantization.
- Compare different quantization bit depths.
- Calculate measured SQNR.
- Display SQNR versus bit-depth graph.
- Listen to quantized audio.
- Visualize quantization noise.

## Technologies Used

- Python
- Streamlit
- NumPy
- SciPy
- Matplotlib
- SoundFile

## Project Structure

```text
PCM-Quantization-Analyzer/
│
├── app.py
├── requirements.txt
├── test_visualization.py
├── .gitignore
│
├── data/
│   └── audio/
│       └── test_audio.wav
│
└── src/
    ├── audio_loader.py
    ├── quantizer.py
    ├── sqnr.py
    └── visualization.py
```

## SQNR Formula

For an ideal uniform quantizer with a full-scale sinusoidal input:

SQNR = 6.02N + 1.76 dB

Where N represents the number of quantization bits.

The application also calculates measured SQNR using the actual audio signal.

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd PCM-Quantization-Analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Objective

To understand PCM quantization, quantization noise, and the relationship between bit depth and digital audio quality through practical experimentation.

## Author

Kartik

Electronics and Communication Engineering