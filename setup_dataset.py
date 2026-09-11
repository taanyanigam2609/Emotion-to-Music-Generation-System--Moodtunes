import os
import urllib.request
import zipfile
import shutil
import ssl  # Added to handle the SSL error

# Bypass SSL certificate verification for this download
ssl._create_default_https_context = ssl._create_unverified_context

# Direct download link for the EMOPIA dataset (MIDI files)
DATASET_URL = "https://github.com/annahung31/EMOPIA/raw/master/dataset/EMOPIA_1.0.zip"
ZIP_FILENAME = "EMOPIA_1.0.zip"
EXTRACT_DIR = "temp_emopia"

QUADRANT_MAP = {
    'Q1': 'happy',  
    'Q2': 'angry',  
    'Q3': 'sad',    
    'Q4': 'calm'    
}

def create_directories():
    print("Checking directory structure...")
    for emotion in QUADRANT_MAP.values():
        path = os.path.join("dataset", emotion)
        os.makedirs(path, exist_ok=True)
        print(f" Ready: {path}")

def download_dataset():
    if not os.path.exists(ZIP_FILENAME):
        print(f"\nDownloading EMOPIA dataset from GitHub...")
        try:
            urllib.request.urlretrieve(DATASET_URL, ZIP_FILENAME)
            print("Download complete!")
        except Exception as e:
            print(f"Failed to download: {e}")
    else:
        print(f"\nFound existing {ZIP_FILENAME}, skipping download.")

def extract_and_sort():
    if not os.path.exists(ZIP_FILENAME):
        return

    print(f"\nExtracting {ZIP_FILENAME}...")
    with zipfile.ZipFile(ZIP_FILENAME, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)
    
    print("\nSorting MIDI files into emotion folders...")
    midi_count = 0
    
    for root, dirs, files in os.walk(EXTRACT_DIR):
        for file in files:
            if file.endswith(".mid"):
                quadrant = file[:2] 
                
                if quadrant in QUADRANT_MAP:
                    target_emotion = QUADRANT_MAP[quadrant]
                    source_path = os.path.join(root, file)
                    target_path = os.path.join("dataset", target_emotion, file)
                    
                    shutil.copy(source_path, target_path)
                    midi_count += 1

    print(f"Successfully sorted {midi_count} MIDI files!")

def cleanup():
    print("\nCleaning up temporary files...")
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    if os.path.exists(ZIP_FILENAME):
        os.remove(ZIP_FILENAME)
    print("Cleanup complete!")

if __name__ == "__main__":
    print("=== MoodTunes Dataset Setup ===")
    create_directories()
    download_dataset()
    extract_and_sort()
    cleanup()
    print("\n Dataset setup is complete!")