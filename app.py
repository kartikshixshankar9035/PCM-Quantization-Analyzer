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
        "Upload a WAV, MP3, M4A, FLAC or OGG audio file to begin PCM quantization analysis."
    )
