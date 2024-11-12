import numpy as np
from pydub import AudioSegment
import random

# Function to generate a single tone
def generate_tone(freq_pair, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = np.sin(freq_pair[0] * 2 * np.pi * t) + np.sin(freq_pair[1] * 2 * np.pi * t)
    tone *= (2**15 - 1) / np.max(np.abs(tone))  # Normalize tone
    return tone.astype(np.int16)

# Generate the "number disconnected" tritone
def generate_sit_tone(sample_rate):
    tones = [950, 1400, 1800]  # Frequencies in Hz
    tone_duration = 330  # Duration of each tone in milliseconds
    pause_duration = 330  # Duration of pause between tones in milliseconds
    
    sit_tone = AudioSegment.silent(duration=0)
    for freq in tones:
        tone_wave = generate_tone((freq, freq), tone_duration / 1000.0, sample_rate)  # Updated to use generate_tone correctly
        tone_segment = AudioSegment(
            tone_wave.tobytes(),
            frame_rate=sample_rate,
            sample_width=tone_wave.dtype.itemsize,
            channels=1
        )
        sit_tone += tone_segment + AudioSegment.silent(duration=pause_duration)
    return sit_tone

# Rest of the script for generating random DTMF tones...
sample_rate = 44100  # Sample rate in Hz
duration = 0.1  # Duration of each tone in seconds
fade_duration = 10  # Duration of the fade in milliseconds
total_duration = 30  # Total duration in seconds

dtmf_freqs = {
    '1': (697, 1209), '2': (697, 1336), '3': (697, 1477),
    '4': (770, 1209), '5': (770, 1336), '6': (770, 1477),
    '7': (852, 1209), '8': (852, 1336), '9': (852, 1477),
    '*': (941, 1209), '0': (941, 1336), '#': (941, 1477),
    'A': (697, 1633), 'B': (770, 1633), 'C': (852, 1633), 'D': (941, 1633),
}

# Generate SIT tone
sit_tone = generate_sit_tone(sample_rate)

# Generate DTMF tones (same as before, now referenced as dtmf_tones)
# Make sure to generate this with the same sample_rate
dtmf_tones = AudioSegment.silent(duration=0)  # Updated variable name for clarity

while len(dtmf_tones) < (total_duration * 1000) - len(sit_tone):
    tone_key = random.choice(list(dtmf_freqs.keys()))
    tone_wave = generate_tone(dtmf_freqs[tone_key], duration, sample_rate)  # Use the original, correct method
    tone_segment = AudioSegment(
        tone_wave.tobytes(),
        frame_rate=sample_rate,
        sample_width=tone_wave.dtype.itemsize,
        channels=1
    ).fade_in(fade_duration).fade_out(fade_duration)
    dtmf_tones += tone_segment

# Prepend the SIT tone to the DTMF sequence
output = sit_tone + dtmf_tones

# Save the output
output.export("random_dtmf_tones_with_sit.wav", format="wav")
