import os
import numpy as np
from pedalboard import (
    Pedalboard, Reverb, Distortion, Delay, Compressor, Gain,
    Chorus, Phaser, HighpassFilter, LowpassFilter, PitchShift
)
from pedalboard.io import AudioFile

# Directory paths
CLEAN_AUDIO_DIR = "./clean_samples"  
PROCESSED_AUDIO_DIR = "./processed_samples"
PARAMETERS_FILE = "effect_params.npy"

# Create processed audio directory if it doesn't exist
os.makedirs(PROCESSED_AUDIO_DIR, exist_ok=True)

# Function to generate random effect parameters
def generate_random_parameters():
    params = {
        "reverb_room_size": np.random.uniform(0.1, 1.0),
        "distortion_gain": np.random.uniform(0.0, 1.0),
        "delay_time": np.random.uniform(0.01, 1.0),
        "delay_mix": np.random.uniform(0.1, 1.0),
        "compressor_threshold": np.random.uniform(-40, 0),
        "gain_db": np.random.uniform(-12, 12),
        "chorus_depth": np.random.uniform(0.1, 0.8),
        "chorus_rate": np.random.uniform(0.1, 2.0),
        "chorus_mix": np.random.uniform(0.1, 0.6),
        "phaser_rate": np.random.uniform(0.1, 0.8),
        "highpass_cutoff": np.random.uniform(20, 1000),
        "lowpass_cutoff": np.random.uniform(2000, 10000),
        "pitch_shift_semitones": np.random.uniform(-8, 8)
    }
    return params

# Function to apply effects
def apply_effects(audio, sample_rate, params):
    board = Pedalboard([
        Reverb(room_size=params["reverb_room_size"]),
        Distortion(drive_db=params["distortion_gain"] * 40),  # Scale to 0-40 dB
        Delay(delay_seconds=params["delay_time"] * 0.5, mix=params["delay_mix"]),  # Scale to 0-0.5 seconds
        Compressor(threshold_db=params["compressor_threshold"]),
        Gain(gain_db=params["gain_db"]),
        Chorus(depth=params["chorus_depth"], rate_hz=params["chorus_rate"], mix=params["chorus_mix"]),
        Phaser(rate_hz=params["phaser_rate"]),
        HighpassFilter(cutoff_frequency_hz=params["highpass_cutoff"]),
        LowpassFilter(cutoff_frequency_hz=params["lowpass_cutoff"]),
        PitchShift(semitones=params["pitch_shift_semitones"])
    ])
    return board(audio, sample_rate)

# Process audio files
effect_parameters = []
for filename in os.listdir(CLEAN_AUDIO_DIR):
    if filename.endswith(".wav"):  
        filepath = os.path.join(CLEAN_AUDIO_DIR, filename)

        # Load clean audio
        with AudioFile(filepath, 'r') as f:
            clean_audio = f.read(f.frames)
            sample_rate = f.samplerate

        # Generate random parameters
        params = generate_random_parameters()

        # Apply effects
        processed_audio = apply_effects(clean_audio, sample_rate, params)

        # Save processed audio
        output_path = os.path.join(PROCESSED_AUDIO_DIR, f"processed_{filename}")
        num_channels = clean_audio.shape[0]
        with AudioFile(output_path, 'w', samplerate=sample_rate, num_channels=num_channels) as f:
            f.write(processed_audio)
        print(f"Processed {filename} and saved to {output_path}")
        # Save parameters
        effect_parameters.append((filename, params))

# Save parameters as a numpy file
np.save(PARAMETERS_FILE, effect_parameters)

print(f"Processed {len(effect_parameters)} samples. Parameters saved to {PARAMETERS_FILE}")