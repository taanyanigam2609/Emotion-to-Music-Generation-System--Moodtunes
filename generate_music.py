import numpy as np
import tensorflow as tf
import os
import traceback
from utils.midi_processing import sequence_to_midi

def generate_fallback_melody(emotion_id, length=120):
    """FAILSAFE: Mathematical fallback in case the AI model crashe or is missing. The app will NEVER break."""
    print("⚠️ WARNING: AI model failed or missing. Engaging fallback generator.")
    pitches = []
    
    # Base scales based on Russell's Circumplex Model
    scales = {
        0: [60, 62, 64, 65, 67, 69, 71, 72], # Happy (C Major)
        1: [57, 59, 60, 62, 64, 65, 67, 69], # Sad (A Minor)
        2: [64, 65, 67, 69, 71, 72, 74, 76], # Angry (E Phrygian)
        3: [65, 67, 69, 71, 72, 74, 76, 77]  # Calm (F Lydian)
    }
    
    base_scale = scales.get(emotion_id, scales[3])
    
    for i in range(length):
        # Generate a semi-random pattern that beautifully stays in key
        idx = (i + np.random.randint(0, 3)) % len(base_scale)
        pitches.append(base_scale[idx])
        
    return pitches

def generate_track(emotion_id, style_id, intensity, temperature=1.0, length=120):
    print(f"\n--- INITIATING AI AUDIO SYNTHESIS ---")
    print(f"Payload -> Emotion: {emotion_id}, Style: {style_id}, Intensity: {intensity}, Creativity: {temperature}")
    
    generated_pitches = []
    
    try:
        # Load the Neural Model with Fallback checks
        model_path = "model/music_generator.keras"
        if not os.path.exists(model_path):
            model_path = "model/music_generator.h5"
            
        if not os.path.exists(model_path):
            # No model found at all. Skip to failsafe.
            raise FileNotFoundError("AI model missing.")

        print(f"Loading neural brain: {model_path}")
        model = tf.keras.models.load_model(model_path)
        
        # 1. Prepare inputs
        current_sequence = np.random.randint(50, 70, size=(1, 50, 1)).astype('float32') / 128.0
        emo_array = np.array([[emotion_id]])
        style_array = np.array([[style_id]])
        
        # 2. Generate
        print("Synthesizing neural sequence...")
        for _ in range(length):
            prediction = model.predict([current_sequence, emo_array, style_array], verbose=0)[0]
            
            # Apply Temperature Creativity peacefully
            prediction = np.log(prediction + 1e-7) / max(temperature, 0.1)
            exp_preds = np.exp(prediction)
            prediction = exp_preds / np.sum(exp_preds)
            
            next_pitch = np.random.choice(range(128), p=prediction)
            generated_pitches.append(next_pitch)
            
            # Update Sequence
            next_pitch_norm = np.array([[[next_pitch / 128.0]]])
            current_sequence = np.append(current_sequence[:, 1:, :], next_pitch_norm, axis=1)

    except Exception as e:
        print("\n❌ AI SYNTHESIS FAILED. ACTIVATING FAILSAFE. ❌")
        traceback.print_exc()
        # Call mathematical fallback so the backend NEVER returns a 500 panic code
        generated_pitches = generate_fallback_melody(emotion_id, length)

    # --- Apply Dynamics, Style, Velocity, Tempo, and Save ---
    try:
        # Affect tempo and strike velocity
        velocity_scale = 0.5 + (float(intensity) / 10.0)
        tempo_multiplier = 0.8 + (float(intensity) / 20.0)
        
        os.makedirs("generated_music", exist_ok=True)
        out_path = f"generated_music/output_e{emotion_id}_s{style_id}.mid"
        
        print("Converting raw sequence to MIDI file...")
        sequence_to_midi(generated_pitches, out_path, tempo_multiplier, velocity_scale)
        
        print(f"✅ SUCCESS! Track saved to: {out_path}")
        print("--------------------------------\n")
        return out_path
    except Exception as save_err:
        print(f"Error during file saving: {save_err}")
        return None