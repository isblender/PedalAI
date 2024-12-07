import numpy as np
from pedalboard import Pedalboard, Reverb, Distortion, Delay, Compressor, Gain, Chorus, Phaser, HighpassFilter, LowpassFilter, PitchShift
from pedalboard.io import AudioStream

def run_effects_live(params):
    """
    Apply audio effects live using Pedalboard and AudioStream.
    
    Args:
        params (dict): Effect parameters dictionary.
    """
    # Define the Pedalboard with the provided parameters
    board = Pedalboard([
        Reverb(room_size=params["reverb_room_size"]),
        Distortion(drive_db=params["distortion_gain"] * 40),
        Delay(delay_seconds=params["delay_time"] * 0.5, mix=params["delay_mix"]),
        Compressor(threshold_db=params["compressor_threshold"]),
        Gain(gain_db=params["gain_db"]),
        Chorus(depth=params["chorus_depth"], rate_hz=params["chorus_rate"], mix=params["chorus_mix"]),
        Phaser(rate_hz=params["phaser_rate"]),
        HighpassFilter(cutoff_frequency_hz=params["highpass_cutoff"]),
        LowpassFilter(cutoff_frequency_hz=params["lowpass_cutoff"]),
        PitchShift(semitones=params["pitch_shift_semitones"])
    ])
    
    # Configure and start the audio stream
    stream = AudioStream(
        input_device_name=AudioStream.input_device_names[0],
        output_device_name=AudioStream.output_device_names[0],
        num_input_channels=1,  # Mono audio; use 2 for stereo
        num_output_channels=1,
        allow_feedback=False,
        buffer_size=1024,
        sample_rate=44100,
    )
    
    stream.plugins = board
    print("Processing live audio with effects. Press Ctrl+C to stop.")
    
    try:
        stream.run()
    except KeyboardInterrupt:
        print("Stopped live audio processing.")

# Example usage
if __name__ == "__main__":
    example_params = {
        "reverb_room_size": 0.5,
        "distortion_gain": 0.2,
        "delay_time": 0.4,
        "delay_mix": 0.3,
        "compressor_threshold": -20,
        "gain_db": 6,
        "chorus_depth": 0.4,
        "chorus_rate": 1.0,
        "chorus_mix": 0.5,
        "phaser_rate": 0.5,
        "highpass_cutoff": 500,
        "lowpass_cutoff": 5000,
        "pitch_shift_semitones": -2
    }
    run_effects_live(example_params)