import tensorflow as tf
from train_model import load_real_data

def evaluate():
    print("Loading the trained neural network...")
    try:
        model = tf.keras.models.load_model("model/music_generator.keras")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("Loading evaluation data...")
    # Loading the data again to test it
    X_notes, X_emos, X_styles, y_pitches = load_real_data()

    if len(X_notes) == 0:
        print("No data found to evaluate.")
        return

    print(f"\nTesting model against {len(X_notes)} musical sequences...")
    
    # model.evaluate returns [loss, accuracy]
    results = model.evaluate([X_notes, X_emos, X_styles], y_pitches, batch_size=64, verbose=1)
    
    print("\n=== EVALUATION RESULTS ===")
    print(f"Loss (Error Rate): {results[0]:.4f}")
    print(f"Accuracy:          {results[1] * 100:.2f}%")

if __name__ == "__main__":
    evaluate()