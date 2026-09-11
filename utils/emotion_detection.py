import cv2
import numpy as np
from deepface import DeepFace
import traceback

def detect_emotion_from_frame(frame_bytes):
    """Ultra-Fast, Error-Proof Emotion Detector with JSON-safe Math."""
    try:
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None or img.size == 0:
            return _fallback_emotion("Empty or corrupted frame.")

        # THE FIX: enforce_detection=False ensures the app doesn't crash 
        # if the room is dark or a face isn't perfectly visible.
        result = DeepFace.analyze(
            img, 
            actions=['emotion'], 
            enforce_detection=False, 
            detector_backend='opencv', 
            silent=True
        )
        
        if isinstance(result, list):
            result = result[0]
            
        dominant = result.get('dominant_emotion', 'neutral')
        
        emotion_mapping = {
            'happy': 0, 'sad': 1, 'angry': 2, 'neutral': 3,
            'fear': 1, 'disgust': 2, 'surprise': 0
        }
        
        # Cast numpy.float32 to standard Python floats so Flask doesn't crash!
        raw_probs = result.get('emotion', {})
        clean_probs = {k: float(v) for k, v in raw_probs.items()}
        
        return {
            'success': True,
            'label': dominant,
            'emotion': dominant, # Added for broader app.py compatibility
            'id': emotion_mapping.get(dominant, 3), 
            'emotion_id': emotion_mapping.get(dominant, 3), # Added for broader app.py compatibility
            'probabilities': clean_probs
        }
        
    except ValueError:
        return _fallback_emotion("No face detected")
    except Exception as e:
        print("\n=== CRITICAL DEEPFACE ERROR ===")
        traceback.print_exc()
        print("===============================\n")
        return _fallback_emotion(f"Internal AI error: {str(e)}")


def detect_emotion_from_text(text):
    """Text Sentiment Analyzer"""
    try:
        if not text:
            return _fallback_emotion("Invalid text input.")
            
        text = text.lower()
        happy_words = ['happy', 'joy', 'excited', 'great', 'awesome', 'good', 'love', 'fantastic', 'amazing']
        sad_words = ['sad', 'depressed', 'down', 'cry', 'tears', 'lonely', 'bad', 'miss', 'heartbreak']
        angry_words = ['angry', 'mad', 'furious', 'hate', 'rage', 'annoyed', 'frustrated', 'pissed']
        
        probs = {'happy': 0.0, 'sad': 0.0, 'angry': 0.0, 'fear': 0.0, 'disgust': 0.0, 'surprise': 0.0, 'neutral': 100.0}
        
        if any(word in text for word in angry_words):
            probs.update({'angry': 100.0, 'neutral': 0.0})
            return {'success': True, 'label': 'angry', 'emotion': 'angry', 'id': 2, 'emotion_id': 2, 'probabilities': probs}
            
        elif any(word in text for word in sad_words):
            probs.update({'sad': 100.0, 'neutral': 0.0})
            return {'success': True, 'label': 'sad', 'emotion': 'sad', 'id': 1, 'emotion_id': 1, 'probabilities': probs}
            
        elif any(word in text for word in happy_words):
            probs.update({'happy': 100.0, 'neutral': 0.0})
            return {'success': True, 'label': 'happy', 'emotion': 'happy', 'id': 0, 'emotion_id': 0, 'probabilities': probs}
            
        else:
            return {'success': True, 'label': 'calm', 'emotion': 'neutral', 'id': 3, 'emotion_id': 3, 'probabilities': probs}
            
    except Exception as e:
        return _fallback_emotion("Text processing failed.")


def _fallback_emotion(reason_str):
    """
    Centralized failsafe that tells the frontend the user is 'neutral'.
    This guarantees the AI music keeps playing even during webcam glitches.
    """
    return {
        "success": True, 
        "label": "neutral",
        "emotion": "neutral",
        "id": 3,
        "emotion_id": 3,
        "probabilities": {'neutral': 100.0},
        "system_debug": reason_str
    }