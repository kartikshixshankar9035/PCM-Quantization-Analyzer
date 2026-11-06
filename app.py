import streamlit as st
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

from io import BytesIO

from src.quantizer import quantize_signal
from src.sqnr import calculate_sqnr


# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="PCM Quantization and Noise Analyzer",
    page_icon="🎧",
    layout="wide"
)

st.title("PCM Quantization and Noise Analyzer")

st.write(
    "Analyze how PCM quantization affects audio quality "
    "at different bit depths."
)

st.divider()


# ==================================================
# 2. AUDIO UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload an audio file (WAV)",
    type=["wav"]
)


if uploaded_file is not None:

    # --------------------------------------------------
    # LOAD AUDIO
    # --------------------------------------------------

    audio, sample_rate = sf.read(
        BytesIO(uploaded_file.getvalue()),
        dtype="float64"
    )

    if audio.ndim == 2:
        audio = np.mean(audio, axis=1)

    if len(audio) == 0:
        st.error("The uploaded audio file is empty.")
        st.stop()

    max_value = np.max(np.abs(audio))

    if max_value > 0:
        audio = audio / max_value

    duration = len(audio) / sample_rate

    # --------------------------------------------------
    # AUDIO INFORMATION
    # --------------------------------------------------

    st.header("1. Audio Information")

    col1, col2, col3 = st.columns(3)

    col1.metric("Sample Rate", f"{sample_rate} Hz")
    col2.metric("Duration", f"{duration:.2f} seconds")
    col3.metric("Total Samples", f"{len(audio):,}")

    st.subheader("Original Audio")

    original_buffer = BytesIO()

    sf.write(
        original_buffer,
        audio,
        sample_rate,
        format="WAV",
        subtype="PCM_16"
    )

    st.audio(original_buffer.getvalue())

    st.divider()

    # --------------------------------------------------
    # PCM QUANTIZATION
    # --------------------------------------------------

    st.header("2. PCM Quantization Analysis")

    results = {}

    for bits in [4, 8, 16]:

        quantized_signal = quantize_signal(audio, bits)

        measured_sqnr = calculate_sqnr(
            audio,
            quantized_signal
        )

        results[bits] = {
            "signal": quantized_signal,
            "sqnr": measured_sqnr
        }

    # --------------------------------------------------
    # MEASURED SQNR
    # --------------------------------------------------

    st.subheader("Measured SQNR")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "4-bit SQNR",
        f"{results[4]['sqnr']:.2f} dB"
    )

    col2.metric(
        "8-bit SQNR",
        f"{results[8]['sqnr']:.2f} dB"
    )

    col3.metric(
        "16-bit SQNR",
        f"{results[16]['sqnr']:.2f} dB"
    )
    # --------------------------------------------------
    # SQNR VS BIT DEPTH GRAPH
    # --------------------------------------------------

    st.subheader("SQNR vs Bit Depth")

    bit_depths = [4, 8, 16]

    sqnr_values = [
        results[bits]["sqnr"]
        for bits in bit_depths
    ]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        bit_depths,
        sqnr_values,
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Bit Depth (bits)")
    ax.set_ylabel("Measured SQNR (dB)")
    ax.set_title("Measured SQNR vs Bit Depth")
    ax.set_xticks(bit_depths)
    ax.grid(True)

    for bits, sqnr in zip(bit_depths, sqnr_values):
        ax.annotate(
            f"{sqnr:.2f} dB",
            (bits, sqnr),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center"
        )

    st.pyplot(fig)
    plt.close(fig)

    st.divider()
        # --------------------------------------------------
    # COMBINED QUANTIZATION ERROR COMPARISON
    # --------------------------------------------------

    st.header("Combined Quantization Error Comparison")

    fig, axes = plt.subplots(
        1, 3,
        figsize=(16, 4)
    )

    for ax, bits in zip(axes, [4, 8, 16]):

        error = audio - results[bits]["signal"]

        ax.hist(
            error,
            bins=50,
            edgecolor="black"
        )

        ax.set_title(f"{bits}-bit Error Distribution")
        ax.set_xlabel("Quantization Error")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.3)

    fig.suptitle(
        "Comparison of Quantization Errors at Different Bit Depths"
    )

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.divider()
    # --------------------------------------------------
    # QUANTIZATION LEVELS
    # --------------------------------------------------

    st.subheader("Quantization Levels")

    level_data = []

    for bits in [4, 8, 16]:

        possible_levels = 2 ** bits

        actual_levels = np.unique(
            results[bits]["signal"]
        ).size

        level_data.append({
            "Bit Depth": f"{bits}-bit",
            "Possible Levels": possible_levels,
            "Actual Levels Used": actual_levels
        })

    st.dataframe(
        level_data,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # THEORETICAL VS MEASURED SQNR
    # --------------------------------------------------

    st.subheader("Theoretical vs Measured SQNR")

    comparison_data = []

    for bits in [4, 8, 16]:

        theoretical_sqnr = 6.02 * bits + 1.76

        comparison_data.append({
            "Bit Depth": f"{bits}-bit",
            "Theoretical SQNR (dB)": round(
                theoretical_sqnr, 2
            ),
            "Measured SQNR (dB)": round(
                results[bits]["sqnr"], 2
            )
        })

    st.dataframe(
        comparison_data,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        """
        Theoretical SQNR is calculated using:

        SQNR = 6.02N + 1.76 dB

        This formula assumes an ideal uniform quantizer
        and a full-scale sinusoidal input.

        Measured SQNR depends on the actual uploaded audio.
        """
    )

    st.divider()

    # --------------------------------------------------
    # QUANTIZED AUDIO PLAYBACK
    # --------------------------------------------------

    st.header("3. Quantized Audio Playback")

    for bits in [4, 8, 16]:

        st.subheader(f"{bits}-bit Quantized Audio")

        audio_buffer = BytesIO()

        sf.write(
            audio_buffer,
            results[bits]["signal"],
            sample_rate,
            format="WAV",
            subtype="PCM_16"
        )

        st.audio(audio_buffer.getvalue())

    st.divider()

    # --------------------------------------------------
    # WAVEFORM ANALYSIS
    # --------------------------------------------------

    st.header("4. Waveform Analysis")

    # Define selected_bits BEFORE using it anywhere else
    selected_bits = st.selectbox(
        "Select bit depth",
        [4, 8, 16],
        index=0
    )

    quantized_signal = results[selected_bits]["signal"]

    samples_to_show = min(
        int(sample_rate * 0.02),
        len(audio)
    )

    time_axis = (
        np.arange(samples_to_show) / sample_rate
    )

    # Original vs quantized waveform
    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        time_axis,
        audio[:samples_to_show],
        label="Original Audio"
    )

    ax.step(
        time_axis,
        quantized_signal[:samples_to_show],
        label=f"{selected_bits}-bit Quantized Audio",
        where="mid"
    )

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Original vs Quantized Waveform")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)

    # --------------------------------------------------
    # QUANTIZATION NOISE
    # --------------------------------------------------

    st.subheader("Quantization Noise")

    noise = audio - quantized_signal

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(
        time_axis,
        noise[:samples_to_show]
    )

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Noise Amplitude")
    ax.set_title(
        f"{selected_bits}-bit Quantization Noise"
    )

    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)

    st.divider()

    # --------------------------------------------------
    # FREQUENCY SPECTRUM ANALYSIS
    # --------------------------------------------------

    st.header("5. Frequency Spectrum Analysis")

    window = np.hanning(len(audio))

    original_windowed = audio * window
    quantized_windowed = quantized_signal * window

    original_fft = np.fft.rfft(original_windowed)
    quantized_fft = np.fft.rfft(quantized_windowed)

    frequencies = np.fft.rfftfreq(
        len(audio),
        d=1 / sample_rate
    )

    scale = np.sum(window)

    original_magnitude = (
        2 * np.abs(original_fft) / scale
    )

    quantized_magnitude = (
        2 * np.abs(quantized_fft) / scale
    )

    epsilon = 1e-12

    original_db = 20 * np.log10(
        np.maximum(original_magnitude, epsilon)
    )

    quantized_db = 20 * np.log10(
        np.maximum(quantized_magnitude, epsilon)
    )

    # Correct DC component
    original_db[0] = 20 * np.log10(
        max(original_magnitude[0] / 2, epsilon)
    )

    quantized_db[0] = 20 * np.log10(
        max(quantized_magnitude[0] / 2, epsilon)
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        frequencies,
        original_db,
        label="Original Audio"
    )

    ax.plot(
        frequencies,
        quantized_db,
        label=f"{selected_bits}-bit Quantized Audio",
        alpha=0.8
    )

    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude (dB)")
    ax.set_title("Frequency Spectrum Comparison")

    ax.legend()
    ax.grid(True)

    st.pyplot(fig)
    plt.close(fig)

    st.divider()
    # --------------------------------------------------
    # QUANTIZATION ERROR HISTOGRAM
    # --------------------------------------------------

    st.subheader("Quantization Error Histogram")

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.hist(
        noise,
        bins=50,
        edgecolor="black"
    )

    ax.set_xlabel("Quantization Error")
    ax.set_ylabel("Frequency")
    ax.set_title(
        f"{selected_bits}-bit Quantization Error Distribution"
    )

    ax.grid(True, alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    st.divider()
    # --------------------------------------------------
    # DOWNLOAD QUANTIZED AUDIO
    # --------------------------------------------------

    st.header("6. Download Quantized Audio")

    download_buffer = BytesIO()

    sf.write(
        download_buffer,
        quantized_signal,
        sample_rate,
        format="WAV",
        subtype="PCM_16"
    )

    st.download_button(
        label=f"Download {selected_bits}-bit Quantized Audio",
        data=download_buffer.getvalue(),
        file_name=f"quantized_{selected_bits}_bit.wav",
        mime="audio/wav"
    )

    st.divider()

    # --------------------------------------------------
    # PROJECT SUMMARY
    # --------------------------------------------------

    st.header("7. Project Summary")

    st.write(f"""
    **Selected Bit Depth:** {selected_bits}-bit

    **Possible Quantization Levels:** {2 ** selected_bits}

    **Actual Levels Used:** {np.unique(quantized_signal).size}

    **Measured SQNR:** {results[selected_bits]['sqnr']:.2f} dB
    """)

    st.success(
        "PCM Quantization and Noise Analysis completed successfully!"
    )


else:

    st.info(
        "Upload a WAV audio file to begin PCM quantization analysis."
    )