import os
import gdown  # DeepFace automatically installed this on your system!
from pathlib import Path
import base64
import traceback
import requests  # This handles GitHub's AWS redirects perfectly


# THE HUGGING FACE DOWNLOADER
def repair_deepface_weights():
    weights_dir = os.path.join(str(Path.home()), ".deepface", "weights")
    weight_file = os.path.join(weights_dir, "facial_expression_model_weights.h5")
    
    os.makedirs(weights_dir, exist_ok=True)
    
    # Check if file exists and is actually the correct size
    if os.path.exists(weight_file):
        size_mb = os.path.getsize(weight_file) / (1024 * 1024)
        if size_mb > 5.0:
            return  # The file is healthy and ready!
        else:
            print(f"⚠️ Corrupted file detected ({size_mb:.2f} MB). Deleting...")
            os.remove(weight_file)
            
    print("📥 Bypassing dead links... Downloading from Hugging Face Mirror (~5.7 MB)...")
    
    # Hugging Face provides unrestricted, raw file access bypassing AWS blocks
    url = "https://huggingface.co/spaces/panik/Facial-Expression/resolve/main/facial_expression_model_weights.h5"
    
    try:
        response = requests.get(url, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
        with open(weight_file, 'wb') as f:
            f.write(response.content)
        print("✅ Weights successfully downloaded from Hugging Face and installed!")
    except Exception as e:
        print(f"❌ Download failed: {e}")

repair_deepface_weights()

# Force compatibility for newer TensorFlow versions
os.environ["TF_USE_LEGACY_KERAS"] = "1" 


# 2. STANDARD FLASK APPLICATION

from flask import Flask, render_template, request, jsonify, send_file
from utils.emotion_detection import detect_emotion_from_frame, detect_emotion_from_text
from generate_music import generate_track

app = Flask(__name__)

# --- PAGE ROUTES ---
@app.route('/')
def index(): return render_template('index.html')
@app.route('/generate')
def generate_page(): return render_template('generate.html')
@app.route('/about')
def about(): return render_template('about.html')
@app.route('/howitworks')
def howitworks(): return render_template('howitworks.html')
@app.route('/faqs')
def faqs(): return render_template('faqs.html')
@app.route('/contact')
def contact(): return render_template('contact.html')

# --- API ROUTES ---
@app.route('/api/detect', methods=['POST'])
def detect():
    try:
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"success": False, "error": "No image payload provided."}), 200
            
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
            
        image_data += "=" * ((4 - len(image_data) % 4) % 4)
            
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as b64_err:
            return jsonify({"success": False, "error": "Corrupted image formatting."}), 200
            
        result = detect_emotion_from_frame(image_bytes)
        return jsonify(result), 200
        
    except Exception as e:
        print(f"CRITICAL Detection API Error: {e}")
        traceback.print_exc()
        return jsonify({"success": False, "error": "Backend server crash protected."}), 200

@app.route('/api/detect_text', methods=['POST'])
def detect_text():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "Empty payload."}), 200
            
        text = data.get('text', '').strip()
        if not text:
            return jsonify({"success": False, "error": "No text provided."}), 200
            
        result = detect_emotion_from_text(text)
        return jsonify(result), 200
        
    except Exception as e:
        print(f"CRITICAL Text API Error: {e}")
        return jsonify({"success": False, "error": "Backend server crash protected."}), 200

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Empty generation payload."}), 400
            
        emotion_id = int(data.get('emotion_id', 3))
        style_id = int(data.get('style_id', 0))
        intensity = float(data.get('intensity', 5.0))
        creativity = float(data.get('creativity', 1.0))
        
        midi_path = generate_track(emotion_id, style_id, intensity, temperature=creativity, length=120)
        
        if midi_path and os.path.exists(midi_path):
            return jsonify({"status": "success", "midi_url": f"/api/download?file={midi_path}"})
            
        return jsonify({"error": "Music engine failed to save the track."}), 500
        
    except Exception as e:
        print(f"CRITICAL Generation API Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal synthesis engine error."}), 500

@app.route('/api/download', methods=['GET'])
def download():
    try:
        file_path = request.args.get('file')
        if file_path and os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return "File not found", 404
    except Exception as e:
        print(f"Download Error: {e}")
        return "File delivery error", 500

if __name__ == '__main__':
    os.makedirs("generated_music", exist_ok=True)
    app.run(debug=True, port=5000)