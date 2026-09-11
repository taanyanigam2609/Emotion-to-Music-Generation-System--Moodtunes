import os
import shutil

# This points to the folder you just dragged in
SOURCE_DIR = "midis" 

QUADRANT_MAP = {
    'Q1': 'happy',
    'Q2': 'angry',
    'Q3': 'sad',
    'Q4': 'calm'
}

def sort_files():
    if not os.path.exists(SOURCE_DIR):
        print(f"❌ Could not find the '{SOURCE_DIR}' folder. Make sure you dragged it into MoodTunes!")
        return

    print("Sorting MIDI files into emotion folders...")
    midi_count = 0
    
    for filename in os.listdir(SOURCE_DIR):
        if filename.endswith(".mid"):
            quadrant = filename[:2]
            
            if quadrant in QUADRANT_MAP:
                target_emotion = QUADRANT_MAP[quadrant]
                target_dir = os.path.join("dataset", target_emotion)
                
                # Ensure the folder exists
                os.makedirs(target_dir, exist_ok=True)
                
                source_path = os.path.join(SOURCE_DIR, filename)
                target_path = os.path.join(target_dir, filename)
                
                shutil.copy(source_path, target_path)
                midi_count += 1
                
    print(f"✅ Successfully sorted {midi_count} MIDI files into the dataset folder!")

if __name__ == "__main__":
    sort_files()