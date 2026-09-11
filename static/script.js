let currentEmotionId = 3;
let generatedMidiUrl = null;
let currentSynth = null;
let currentPart = null; // NEW: Controls the scheduled Part music notes timeline
let animationId = null;
let webcamInterval = null;
let activeInputMode = 'webcam';
let isAudioLoaded = false;

// --- MULTI-TAB NAVIGATION ---
function switchTab(tabId) {
    if (!document.getElementById(tabId)) return;
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-btn.active').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if(btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(tabId)) {
            btn.classList.add('active');
        }
    });
}

// --- INPUT TYPE SWITCHER ---
function switchInputType(type) {
    activeInputMode = type;
    // CRITICAL: Strict stop of webcam polling loop if switching to a different mode
    if (webcamInterval) { clearInterval(webcamInterval); webcamInterval = null; }

    document.querySelectorAll('.input-type-selector button').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');

    // Toggle Visibility Boxes
    document.getElementById('webcamBox').style.display = type === 'webcam' ? 'block' : 'none';
    document.getElementById('uploadBox').style.display = type === 'upload' ? 'block' : 'none';
    document.getElementById('textBox').style.display = type === 'text' ? 'block' : 'none';

    // Restart webcam polling ONLY if returning to webcam mode
    if (type === 'webcam') startWebcamPolling();
}

// --- SLIDER UPDATES ---
document.getElementById('intensity')?.addEventListener('input', (e) => document.getElementById('val-intensity').innerText = e.target.value);
document.getElementById('creativity')?.addEventListener('input', (e) => document.getElementById('val-creativity').innerText = e.target.value);

// --- RADAR CHART INITIALIZATION ---
const chartCanvas = document.getElementById('emotionChart');
let emotionChart;
if(chartCanvas) {
    const ctx = chartCanvas.getContext('2d');
    emotionChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Happy', 'Sad', 'Angry', 'Fear', 'Disgust', 'Surprise', 'Neutral'],
            datasets: [{
                label: 'Emotional Signature',
                data: [0,0,0,0,0,0,0],
                backgroundColor: 'rgba(0, 240, 255, 0.2)',
                borderColor: '#00f0ff',
                pointBackgroundColor: '#8a2be2',
                borderWidth: 2
            }]
        },
        options: {
            scales: { r: { pointLabels: { color: 'rgba(255,255,255,0.8)' }, ticks: { display: false, max: 100 } } },
            plugins: { legend: { display: false } },
            maintainAspectRatio: false
        }
    });
}

function updateChartAndUI(data) {
    if (!data) return;
    const emSpan = document.getElementById('currentEmotion');
    emSpan.innerText = data.label.toUpperCase();
    emSpan.classList.remove('blink');
    currentEmotionId = data.id;
    
    if (emotionChart) {
        // Ensure data points always map properly even if backend values vary
        emotionChart.data.datasets[0].data = [
            data.probabilities.happy || 0, data.probabilities.sad || 0, data.probabilities.angry || 0, 
            data.probabilities.fear || 0, data.probabilities.disgust || 0, data.probabilities.surprise || 0, data.probabilities.neutral || 0
        ];
        emotionChart.update();
    }
}

// --- 1. WEBCAM LOGIC ---
const video = document.getElementById('webcam');
if (video) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => { video.srcObject = stream; if (activeInputMode === 'webcam') startWebcamPolling(); })
        .catch(err => { document.getElementById('currentEmotion').innerText = "Camera Denied"; document.getElementById('currentEmotion').classList.remove('blink'); });
}

function startWebcamPolling() {
    if (webcamInterval) clearInterval(webcamInterval);
    webcamInterval = setInterval(async () => {
        // Ensure frame has actual pixels before sending to backend
        if (!video || video.readyState !== 4 || activeInputMode !== 'webcam' || video.videoWidth === 0) return;
        
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth; canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        
        try {
            const res = await fetch('/api/detect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ image: canvas.toDataURL('image/jpeg') })
            });
            if (res.ok) updateChartAndUI(await res.json());
        } catch (e) {}
    }, 2000); // 2 second polling interval
}

// --- 2. ADVANCED IMAGE UPLOAD & COMPRESSION LOGIC ---
document.getElementById('imageUpload')?.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Update UI State
    const emSpan = document.getElementById('currentEmotion');
    emSpan.innerText = "Compressing & Analyzing...";
    emSpan.classList.add('blink');

    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = async function() {
            // ADVANCED LEVEL: Compress image via Canvas before sending to Flask
            const canvas = document.createElement('canvas');
            const MAX_WIDTH = 640; // Force downscale to 640px width for blazing speed
            const scaleSize = MAX_WIDTH / img.width;
            
            canvas.width = MAX_WIDTH;
            canvas.height = img.height * scaleSize;
            
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            
            // Extract compressed Base64 JPEG at 80% quality
            const compressedBase64 = canvas.toDataURL('image/jpeg', 0.8);
            
            // Show preview instantly
            document.getElementById('uploadPreview').src = compressedBase64;
            document.getElementById('uploadPreview').style.display = 'block';

            try {
                // Send the tiny, compressed payload to backend
                const res = await fetch('/api/detect', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ image: compressedBase64 })
                });
                
                if (res.ok) {
                    const data = await res.json();
                    if (data.success) {
                        updateChartAndUI(data);
                    } else {
                        // Display exact error (e.g. "No Face Found") without crashing
                        emSpan.innerText = data.error || "No Face Detected";
                        emSpan.classList.remove('blink');
                    }
                } else {
                    emSpan.innerText = "Server Timeout/Error";
                    emSpan.classList.remove('blink');
                }
            } catch (err) {
                console.error("Upload Network Error:", err);
                emSpan.innerText = "Network Error";
                emSpan.classList.remove('blink');
            }
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
});

// --- 3. TEXT SENTIMENT LOGIC ---
document.getElementById('analyzeTextBtn')?.addEventListener('click', async () => {
    const text = document.getElementById('textInput').value;
    if (!text) return;
    document.getElementById('currentEmotion').innerText = "Analyzing Text...";
    document.getElementById('currentEmotion').classList.add('blink');

    const res = await fetch('/api/detect_text', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ text: text })
    });
    if (res.ok) updateChartAndUI(await res.json());
});

// --- MUSIC GENERATION LOGIC ---
const generateBtn = document.getElementById('generateBtn');
if(generateBtn) {
    generateBtn.addEventListener('click', async () => {
        const btn = document.getElementById('generateBtn');
        const loader = document.getElementById('loadingIndicator');
        
        // Secure UI State immediately
        btn.style.display = 'none';
        loader.style.display = 'block';
        
        // FIXED: ADDED EXPLICIT JSON TYPE CASTING to prevent 500 parse errors on payload
        const payload = {
            emotion_id: parseInt(currentEmotionId),
            style_id: parseInt(document.getElementById('style').value),
            intensity: parseFloat(document.getElementById('intensity').value),
            creativity: parseFloat(document.getElementById('creativity').value)
        };
        
        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Add Cache-Buster timestamp so the browser always downloads the new tune
                generatedMidiUrl = data.midi_url + "&t=" + new Date().getTime();
                
                // Reset audio state for the new track
                isAudioLoaded = false;
                document.getElementById('playBtn').innerText = "▶ Play Sequence";
                
                document.getElementById('playerControls').style.opacity = '1';
                document.getElementById('playerControls').style.pointerEvents = 'all';
                document.getElementById('downloadBtn').href = generatedMidiUrl;
                
                // Smooth transition to audio player tab
                switchTab('visualizer');
            } else {
                const errData = await response.json();
                console.error("Backend Error:", errData);
                alert(`Error: ${errData.error || "Generation engine encountered an issue."}`);
            }
        } catch(e) {
            console.error("Fetch Error:", e);
            alert("Network error. Could not connect to the engine.");
        } finally {
            // Restore UI no matter what
            btn.style.display = 'block';
            loader.style.display = 'none';
        }
    });
}

// --- TRUE AUDIO STATE CONTROLLER & VISUALIZER ---
const audioCanvas = document.getElementById('audioCanvas');
let audioCtx, analyser;

// Add Master Audio Channel Processing to prevent noise clipping
const masterLimiter = new Tone.Limiter(-5).toDestination();
const masterReverb = new Tone.Freeverb({ roomSize: 0.7, dampening: 4000 }).connect(masterLimiter);

if(audioCanvas) {
    audioCtx = audioCanvas.getContext('2d');
    analyser = new Tone.Analyser("waveform", 512);
    analyser.connect(masterReverb);
}

function drawWaveform() {
    animationId = requestAnimationFrame(drawWaveform);
    const values = analyser.getValue();
    
    // Fit canvas dynamically to parent
    audioCanvas.width = audioCanvas.parentElement.clientWidth;
    
    audioCtx.clearRect(0, 0, audioCanvas.width, audioCanvas.height);
    audioCtx.beginPath();
    audioCtx.strokeStyle = "#00f0ff";
    audioCtx.lineWidth = 4;
    audioCtx.shadowBlur = 15;
    audioCtx.shadowColor = "#8a2be2";

    for (let i = 0; i < values.length; i++) {
        const x = (i / values.length) * audioCanvas.width;
        const y = (0.5 + values[i] / 2) * audioCanvas.height;
        if (i === 0) audioCtx.moveTo(x, y);
        else audioCtx.lineTo(x, y);
    }
    audioCtx.stroke();
}

document.getElementById('playBtn')?.addEventListener('click', async () => {
    if (!generatedMidiUrl) return;
    const playBtn = document.getElementById('playBtn');
    
    // 1. True Pause Logic
    if (Tone.Transport.state === "started") {
        Tone.Transport.pause();
        // Force the synth to silence echoing notes immediately
        if (currentSynth) currentSynth.releaseAll(); 
        playBtn.innerText = "▶ Resume Sequence";
        cancelAnimationFrame(animationId);
        return;
    }
    
    // 2. True Resume Logic
    if (Tone.Transport.state === "paused" && isAudioLoaded) {
        Tone.Transport.start();
        playBtn.innerText = "⏸ Pause Sequence";
        drawWaveform();
        return;
    }
    
    // 3. Initial Play Logic (Requires binding notes to Tone.Part timeline)
    await Tone.start();
    Tone.Transport.stop();
    Tone.Transport.cancel();
    
    if (currentPart) currentPart.dispose();
    if (currentSynth) currentSynth.dispose();
    
    const midi = await Midi.fromUrl(generatedMidiUrl);
    
    // Smoother instruments to prevent noise/clipping
    const instType = document.getElementById('instrument') ? document.getElementById('instrument').value : 'piano';
    if (instType === 'synth') {
        currentSynth = new Tone.PolySynth(Tone.Synth, { oscillator: { type: "sine" }, envelope: { attack: 0.1, decay: 0.2, sustain: 0.5, release: 1 } });
    } else if (instType === 'pluck') {
        currentSynth = new Tone.PolySynth(Tone.PluckSynth);
    } else {
        currentSynth = new Tone.PolySynth(Tone.AMSynth);
    }
    currentSynth.connect(analyser);
    
    // Bundle all tracks into a single timeline array for Tone.Part
    let allNotes = [];
    midi.tracks.forEach(track => {
        track.notes.forEach(note => {
            allNotes.push({ time: note.time, name: note.name, duration: note.duration, velocity: note.velocity });
        });
    });
    
    // PART SYSTEM: Notes explicitly linked to Tone Transport controls for true pause/stop
    currentPart = new Tone.Part((time, note) => {
        currentSynth.triggerAttackRelease(note.name, note.duration, time, note.velocity);
    }, allNotes).start(0);
    
    isAudioLoaded = true;
    Tone.Transport.start();
    playBtn.innerText = "⏸ Pause Sequence";
    drawWaveform();
});

document.getElementById('stopBtn')?.addEventListener('click', () => {
    // True full stop and reset logic
    Tone.Transport.stop();
    Tone.Transport.cancel(); // Clears scheduled notes
    
    if (currentPart) {
        currentPart.dispose();
        currentPart = null;
    }
    if (currentSynth) {
        currentSynth.releaseAll(); // Silence all notes immediately
        currentSynth.dispose();
        currentSynth = null;
    }
    
    isAudioLoaded = false;
    document.getElementById('playBtn').innerText = "▶ Play Sequence";
    
    cancelAnimationFrame(animationId);
    audioCtx.clearRect(0, 0, audioCanvas.width, audioCanvas.height);
    audioCtx.beginPath();
    audioCtx.strokeStyle = "#444";
    audioCtx.moveTo(0, audioCanvas.height / 2);
    audioCtx.lineTo(audioCanvas.width, audioCanvas.height / 2);
    audioCtx.stroke();
});