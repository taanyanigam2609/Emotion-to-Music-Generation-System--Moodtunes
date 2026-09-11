# Emotion-to-Music-Generation-System--Moodtunes

MoodTunes is an AI-powered music generation web application that creates emotion-aware music using a **Conditional Long Short-Term Memory (LSTM) deep learning model**. The system allows users to either manually select an emotion such as **Happy, Sad, Angry, or Calm** or detect their emotion through a **webcam-based facial emotion recognition system**. Based on the detected or selected emotion, the trained model generates a unique symbolic music sequence and converts it into a playable **MIDI file**.

The application provides an interactive, multi-page web interface where users can generate, visualize, play, and download AI-generated music. MoodTunes combines **Deep Learning, Emotion Recognition, Symbolic Music Generation, Flask, JavaScript, and MIDI processing** into a single end-to-end platform.

---

### **Project Overview**

**Title:** MoodTunes: AI-Based Emotion-to-Music Generation Using Conditional Deep Learning

**Objective:** To develop an intelligent music generation system that learns musical patterns associated with different emotions and automatically generates emotion-aware MIDI music based on the user's selected or webcam-detected emotional state.

The system combines **facial emotion recognition** with **conditional music generation**, enabling users to create personalized music without requiring musical composition expertise.

---

### **How to Run the Project**


**Step 1: Clone or Download the Project**

```bash
git clone https://github.com/[yourusername]/MoodTunes.git
cd MoodTunes
```

**Step 2: Create a Virtual Environment**

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

**Step 3: Install Dependencies**

Make sure Python 3.9+ is installed. Then run:

```bash
pip install -r requirements.txt
```

**Step 4: Verify Project Structure**

Ensure your directory looks like this:

```text
MoodTunes/
│
├── app.py
├── train_model.py
├── generate_music.py
├── requirements.txt
├── README.md
│
├── dataset/
│   ├── happy/
│   ├── sad/
│   ├── angry/
│   └── calm/
│
├── model/
│   ├── music_generator.keras
│   └── metadata.json
│
├── generated_music/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── script.js
│   │   ├── webcam.js
│   │   ├── visualizer.js
│   │   └── player.js
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── generate.html
│   ├── about.html
│   ├── howitworks.html
│   ├── faqs.html
│   ├── contact.html
│   └── result.html
│
└── utils/
    ├── midi_processing.py
    ├── emotion_detection.py
    └── midi_generation.py
```

**Step 5: Prepare the Dataset**

Download and organize the emotion-labeled MIDI dataset according to the dataset structure described below.

```text
dataset/
├── happy/
├── sad/
├── angry/
└── calm/
```

**Step 6: Train the Model**

Run:

```bash
python train_model.py
```

The trained Conditional LSTM model will be saved inside:

```text
model/
```

**Step 7: Run the Flask Application**

Execute:

```bash
python app.py
```

**Step 8: Access the Web Interface**

Open your browser and go to:

```text
http://127.0.0.1:5000/
```

**Step 9: Use the Application**

Users can:

* Select an emotion manually from the dropdown.
* Enable webcam-based emotion detection.
* Detect facial emotion using the webcam.
* View emotion probabilities.
* Adjust emotion intensity.
* Select music style/instrument.
* Adjust tempo and music length.
* Generate emotion-based music.
* Play the generated MIDI music.
* Visualize the generated music.
* Download the generated MIDI file.

---

### **Dataset Details**


MoodTunes uses **symbolic music datasets containing MIDI files**. The primary training data should consist of MIDI compositions associated with emotional labels.

Potential datasets include:

* **EMOPIA** – emotion-labeled symbolic piano music and particularly relevant for the emotion-conditioning component.
* **Lakh MIDI Dataset** – large-scale collection of MIDI files useful for expanding the symbolic music corpus.
* **MAESTRO Dataset** – high-quality piano performances in MIDI format.
* **VGMIDI / video-game MIDI collections** – useful for game-oriented musical patterns.

For the project, the MIDI files are organized according to their emotion:

```text
dataset/
│
├── happy/
│   ├── happy_001.mid
│   ├── happy_002.mid
│   └── ...
│
├── sad/
│   ├── sad_001.mid
│   ├── sad_002.mid
│   └── ...
│
├── angry/
│   ├── angry_001.mid
│   ├── angry_002.mid
│   └── ...
│
└── calm/
    ├── calm_001.mid
    ├── calm_002.mid
    └── ...
```

**Dataset Format:** `.mid` / `.midi`

**Data Type:** Symbolic music

**Labels:** Happy, Sad, Angry, Calm

**Musical Features:** Notes, pitch, duration, velocity, tempo and timing information.

> **Important:** The final dataset should preserve reliable emotion labels. If a dataset does not contain emotion annotations, it should not simply be assumed to represent a particular emotion; it must be labeled using a documented annotation strategy.

---

### **Algorithm And Process Design**


* **Model Type:** Conditional LSTM-based symbolic music generator
* **Learning Type:** Supervised sequence learning
* **Generation Type:** Emotion-conditioned music generation
* **Input:** Musical note sequence + emotion condition
* **Output:** Predicted next musical event/note
* **Music Representation:** MIDI symbolic representation
* **Emotion Recognition:** Facial emotion recognition using webcam
* **Backend:** Flask
* **Playback:** JavaScript MIDI/audio playback

The overall pipeline is:

```text
MIDI Dataset
      ↓
Dataset Organization
      ↓
MIDI Preprocessing
      ↓
Note / Chord / Timing Extraction
      ↓
Numerical Encoding
      ↓
Training Sequences
      ↓
Emotion Encoding
      ↓
Conditional LSTM
      ↓
Next-Note Prediction
      ↓
Music Sequence Generation
      ↓
MIDI Reconstruction
      ↓
Browser Playback
```

---

### **Details Of Hardware And Software**


* **Hardware:** Computer/laptop with multi-core CPU, minimum 8 GB RAM, 16 GB+ recommended for larger datasets, SSD storage for MIDI datasets and trained models, and webcam for facial emotion detection.
* **Optional:** NVIDIA GPU with CUDA support for faster deep learning training.

**Software Requirements:**

* **Programming Language:** Python
* **Web Framework:** Flask
* **Deep Learning:** TensorFlow / Keras
* **Music Processing:** pretty_midi, music21, Mido
* **Numerical Processing:** NumPy
* **Emotion Recognition:** OpenCV + DeepFace
* **Frontend:** HTML5, CSS3, JavaScript
* **Music Playback:** Tone.js / MIDI.js
* **Visualization:** Chart.js / JavaScript Canvas
* **Development Environment:** VS Code / PyCharm
* **Browser:** Google Chrome / Microsoft Edge

---

### **Key Components**


**1. Dataset Preparation**

Emotion-labeled MIDI files are collected and organized into emotion-specific categories. The dataset provides musical examples corresponding to different emotional states.

---

**2. MIDI Preprocessing**

MIDI files are processed using `pretty_midi` and/or `music21`.

The preprocessing pipeline extracts:

* Pitch
* Note duration
* Note start time
* Note velocity
* Tempo
* Chord information
* Musical sequences

The extracted musical events are converted into numerical representations suitable for deep learning.

---

**3. Sequence Creation**

The continuous musical data is divided into fixed-length sequences.

For example:

```text
Input:
C → D → E → G → A

Target:
C
```

The model learns to predict the next musical event based on previously generated events.

---

**4. Emotion Conditioning**

Each sequence is associated with an emotion label:

```text
Happy → 0
Sad   → 1
Angry → 2
Calm  → 3
```

The emotion information is incorporated into the neural network as a conditioning input.

Conceptually:

```text
Note Sequence ──────┐
                    ├──→ Conditional LSTM ──→ Next Note
Emotion ────────────┘
```

This allows the same model to learn different musical characteristics for different emotions.

---

**5. Conditional LSTM Model**

The core music generation model uses an LSTM architecture designed for sequential musical data.

A typical architecture consists of:

```text
Note Input
     ↓
Note Embedding
     ↓
LSTM Layer
     ↓
LSTM Layer
     ↓
Emotion Embedding
     ↓
Feature Fusion
     ↓
Dense Layers
     ↓
Softmax Output
     ↓
Next Musical Event
```

The model learns temporal relationships between musical events while using the emotion condition to influence generation.

The trained model is saved inside:

```text
model/music_generator.keras
```

---

**6. Music Generation**

When the user selects or detects an emotion, the backend sends the emotion condition to the trained model.

The model generates a sequence iteratively:

```text
Seed Notes
     ↓
Predict Next Note
     ↓
Add Note
     ↓
Predict Next Note
     ↓
Repeat
     ↓
Complete Music Sequence
```

The resulting sequence is converted into a MIDI file using `pretty_midi`.

---

**7. Webcam Emotion Detection**

The application provides a webcam-based emotion detection system.

```text
Webcam
   ↓
Face Detection
   ↓
Facial Expression Analysis
   ↓
Emotion Prediction
   ↓
Emotion Probability
   ↓
MoodTunes Generator
```

Supported emotions are mapped to the music-generation categories:

```text
Happy
Sad
Angry
Calm
```

The detected emotion is then automatically passed to the music generation system.

---

**8. Emotion Selection**

Users can also manually select an emotion through the frontend.

Example:

```text
Choose Your Mood

😊 Happy
😢 Sad
😡 Angry
😌 Calm
```

This provides a fallback when users do not want to use the webcam.

---

**9. Emotion Intensity Control**

An optional emotion intensity slider allows users to control the strength of the selected emotion.

```text
Emotion Intensity
1 ─────────────── 10
```

Intensity can influence musical parameters such as:

* Tempo
* Note density
* Velocity
* Rhythmic activity

For example:

```text
Happy + Low Intensity
→ Soft, relaxed cheerful music

Happy + High Intensity
→ Fast, energetic cheerful music
```

---

**10. Music Style and Instrument Control**

The application can provide additional generation controls such as:

* Piano
* Classical
* Ambient
* Lo-Fi
* Game Music

Users can also select an instrument and adjust the generated music characteristics.

---

**11. Flask Web Application**

Flask acts as the central backend connecting the frontend, emotion recognition system and deep learning model.

Main routes include:

```text
/
 /generate
 /detect_emotion
 /download
```

The backend:

* receives user input,
* processes the selected/detected emotion,
* invokes the generation model,
* creates MIDI output,
* returns the generated file to the frontend.

---

**12. Frontend Multi-Page Interface**

MoodTunes contains a complete multi-tab website:

```text
Home
Generate Music
About Us
How It Works
FAQs
Contact Us
```

The `base.html` template provides the common:

* Navigation bar
* Footer
* CSS/JavaScript imports
* Page layout

Individual pages extend the base template.

---

**13. Music Visualization**

The generated music can be accompanied by an interactive visualization using JavaScript.

The interface can display:

* Animated waveform
* Piano-roll style visualization
* Music activity
* Playback progress
* Emotion information

This improves the user's interaction with the generated music.

---

**14. MIDI Playback And Download**

After generation, users can:

* Play the generated music.
* Stop playback.
* View generation information.
* Download the generated `.mid` file.

Example:

```text
Generated Music
────────────────────────

Emotion: Happy
Style: Piano
Tempo: 120 BPM

▶ Play     ■ Stop     ↓ Download
```

---

### **Results Summary**


* Generates symbolic music conditioned on the selected emotion.
* Supports both manual emotion selection and webcam-based emotion detection.
* Learns sequential musical patterns using a Conditional LSTM model.
* Produces downloadable MIDI files.
* Provides interactive browser-based music playback.
* Provides emotion probability visualization.
* Allows users to customize music parameters such as tempo, intensity and instrument.
* Provides an integrated multi-page web interface for an end-to-end AI music generation experience.

For academic evaluation, model performance should additionally be reported using measurable metrics such as **training/validation loss, sequence prediction accuracy or perplexity where applicable, and human evaluation of emotional alignment and musical quality** rather than claiming accuracy without experimental evidence.

---

### **Applications**


* 🎮 **Emotion-Aware Game Music** – Generate adaptive background music according to game situations or player emotion.
* 🧘 **Relaxation and Wellness** – Generate calm and soothing music.
* 🎬 **Content Creation** – Assist creators in producing mood-specific background music.
* 🎵 **Personalized Music Generation** – Create music based on an individual's current emotional state.
* 🧠 **Emotion-Aware Interactive Systems** – Integrate emotional music generation into intelligent applications.
* 🎨 **Creative Assistance** – Help users experiment with musical ideas without requiring professional composition skills.
* 📱 **Interactive Entertainment** – Create dynamically changing music experiences.

---

### **Future Enhancements**


* **Transformer-Based Music Generation:** Replace or complement the Conditional LSTM with a Transformer architecture for improved long-range musical dependency modeling.
* **Multimodal Emotion Detection:** Combine facial expressions, text sentiment and voice emotion for more robust emotion recognition.
* **Real-Time Adaptive Music:** Continuously monitor the user's emotional state and dynamically modify the generated music.
* **Advanced Music Representation:** Generate richer sequences containing pitch, duration, velocity, chords and tempo instead of predicting pitch alone.
* **Genre Conditioning:** Allow simultaneous conditioning on emotion and musical genre.
* **Audio Generation:** Extend MIDI generation into waveform/audio generation using neural audio synthesis models.
* **Personalized Generation:** Allow the system to learn individual user preferences and generate personalized music.
* **Cloud Deployment:** Deploy the system using cloud infrastructure for scalable music generation.
* **Mobile Application:** Extend MoodTunes to Android and iOS.
* **Music Quality Evaluation:** Incorporate automated musical-quality metrics and human evaluation to measure coherence, diversity and emotional consistency.
* **Reinforcement Learning:** Explore reward-based optimization to improve emotional alignment and musical structure.

---

### **Project Highlights**

```text
🎵 Emotion-Aware AI Music Generation
🧠 Conditional LSTM Deep Learning
😊 Webcam Facial Emotion Detection
🎚️ Emotion Intensity Control
🎹 MIDI Symbolic Music Generation
🎧 Browser-Based Music Playback
📊 Emotion Probability Visualization
🎨 Music Visualization
🌐 Flask Multi-Page Web Application
⬇️ MIDI Download
```

**MoodTunes combines Deep Learning + Computer Vision + Music AI + Web Development into one end-to-end intelligent creative system.**
