import numpy as np
import tensorflow as tf
import os
from utils.midi_processing import extract_notes

SEQ_LEN = 50
NUM_PITCHES = 128
NUM_EMOTIONS = 4
NUM_STYLES = 5

EMOTION_MAP = {'happy': 0, 'sad': 1, 'angry': 2, 'calm': 3}

def build_conditional_lstm():
    # Calling Input and layers directly from tf.keras
    note_input = tf.keras.Input(shape=(SEQ_LEN, 1), name='note_input')
    emo_input = tf.keras.Input(shape=(1,), name='emotion_input')
    style_input = tf.keras.Input(shape=(1,), name='style_input')

    # INCREASED EMBEDDING DIMENSIONS for richer context
    emo_emb = tf.keras.layers.Embedding(NUM_EMOTIONS, 32)(emo_input)
    style_emb = tf.keras.layers.Embedding(NUM_STYLES, 32)(style_input)
    
    emo_rep = tf.keras.layers.RepeatVector(SEQ_LEN)(emo_emb[:, 0, :])
    style_rep = tf.keras.layers.RepeatVector(SEQ_LEN)(style_emb[:, 0, :])
    
    concat = tf.keras.layers.Concatenate(axis=-1)([note_input, emo_rep, style_rep])
    
    # INCREASED CAPACITY: 128 -> 512 units
    x = tf.keras.layers.LSTM(512, return_sequences=True)(concat)
    x = tf.keras.layers.Dropout(0.3)(x)
    x = tf.keras.layers.LSTM(512)(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    
    # ADDED HIDDEN DENSE LAYER for extra pattern recognition
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    
    output = tf.keras.layers.Dense(NUM_PITCHES, activation='softmax', name='pitch_output')(x)
    
    model = tf.keras.Model(inputs=[note_input, emo_input, style_input], outputs=output)
    
    # Explicitly defining the optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model

def load_real_data():
    print("Loading MIDI files... this may take a few minutes.")
    X_notes, X_emos, X_styles, y_pitches = [], [], [], []
    
    base_dir = "dataset"
    for emotion_name, emo_id in EMOTION_MAP.items():
        emo_dir = os.path.join(base_dir, emotion_name)
        if not os.path.exists(emo_dir):
            continue
            
        for filename in os.listdir(emo_dir):
            if filename.endswith(".mid"):
                filepath = os.path.join(emo_dir, filename)
                pitches = extract_notes(filepath)
                
                if pitches is not None and len(pitches) > SEQ_LEN:
                    for i in range(0, len(pitches) - SEQ_LEN):
                        seq_in = pitches[i:i + SEQ_LEN]
                        seq_out = pitches[i + SEQ_LEN]
                        
                        X_notes.append(np.array(seq_in).reshape(SEQ_LEN, 1) / 128.0)
                        X_emos.append(emo_id)
                        X_styles.append(0) 
                        y_pitches.append(seq_out)
                        
    return np.array(X_notes), np.array(X_emos), np.array(X_styles), np.array(y_pitches)

if __name__ == "__main__":
    print("Building and compiling advanced model...")
    model = build_conditional_lstm()
    
    X_notes, X_emos, X_styles, y_pitches = load_real_data()
    
    if len(X_notes) == 0:
        print("No MIDI data found! Did you run setup_dataset.py?")
    else:
        print(f"Successfully loaded {len(X_notes)} training sequences. Starting deep training...")
        
        os.makedirs("model", exist_ok=True)
        model_path = "model/music_generator.keras"
        
        # SMART CALLBACK 1: Save the model only when accuracy hits a new high score
        checkpoint = tf.keras.callbacks.ModelCheckpoint(
            filepath=model_path,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
            verbose=1
        )
        
        # SMART CALLBACK 2: Stop training if the model stops improving for 15 epochs
        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=15,
            restore_best_weights=True,
            verbose=1
        )
        
        # INCREASED EPOCHS (100) AND BATCH SIZE (128)
        model.fit(
            [X_notes, X_emos, X_styles], y_pitches, 
            epochs=100, 
            batch_size=128, 
            validation_split=0.2,
            callbacks=[checkpoint, early_stopping]
        )
        
        print(f"Training complete. Absolute best model weights are secured at {model_path}")