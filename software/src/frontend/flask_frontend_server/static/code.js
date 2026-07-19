// --- WEBSOCKET & TIMING PARAMETERS, Created with llms ---
const WEBSOCKET_URL = "wss://192.168.68.97:5555/stream"; 
const SEND_INTERVAL_MS = 150; // Change this number! (2000ms = every 2 seconds)

const webcamVideo = document.getElementById("webcamVideo");
const flipBtn = document.getElementById("flipBtn");
const captureBtn = document.getElementById("captureBtn");
const trackBtn = document.getElementById("trackBtn"); 
const captureCanvas = document.getElementById("captureCanvas");
const previewContainer = document.getElementById("previewContainer");
const photoPreview = document.getElementById("photoPreview");

// UI ELEMENTS FOR TIMER
const timerSelect = document.getElementById("timerSelect"); 
const countdownDisplay = document.getElementById("countdownDisplay"); 

let currentStream = null;
let currentFacingMode = "user"; 
let streamIntervalId = null; 
let isTrackingActive = false; 

// --- SETUP WEBSOCKET CLIENT ---
const socket = new WebSocket(WEBSOCKET_URL);
socket.binaryType = 'arraybuffer'; 

socket.onopen = () => {
    console.log("Connected to Python Server!");
};

socket.onerror = (error) => {
    console.error("WebSocket Error: ", error);
};

socket.onclose = () => {
    console.log("Disconnected from Python Server.");
    stopStreamingLoop();
};

function startCamera(facingMode) {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
    }

    const constraints = {
        video: {
            width: { ideal: 1920 },
            height: { ideal: 1080 },
            aspectRatio: { ideal: 1.7777777778 },
            facingMode: facingMode 
        }
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {
            currentStream = stream;
            webcamVideo.srcObject = stream;
            
            if (facingMode === "user") {
                webcamVideo.style.transform = "scaleX(1)";
            } else {
                webcamVideo.style.transform = "scaleX(1)";
            }
        })
        .catch(error => {
            console.error("Error accessing the webcam:", error);
        });
}

// --- AUTOMATED FRAME STREAMING FUNCTION ---
function streamFrame() {
    if (socket.readyState !== WebSocket.OPEN) return;
    if (!webcamVideo.videoWidth || !webcamVideo.videoHeight) return;

    const ctx = captureCanvas.getContext("2d");
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    captureCanvas.width = webcamVideo.videoWidth;
    captureCanvas.height = webcamVideo.videoHeight;

    if (currentFacingMode === "user") {
        ctx.translate(captureCanvas.width, 0);
        ctx.scale(-1, 1);
    }

    ctx.drawImage(webcamVideo, 0, 0, captureCanvas.width, captureCanvas.height);

    captureCanvas.toBlob((blob) => {
        if (!blob || socket.readyState !== WebSocket.OPEN) return;
        socket.send(blob);
    }, "image/jpeg", 0.6); 
}

// Toggle camera mode
flipBtn.addEventListener("click", () => {
    currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
    startCamera(currentFacingMode);
});

// Helper to fully clear and reset the tracking stream back to initial idle states
function stopStreamingLoop() {
    clearInterval(streamIntervalId);
    streamIntervalId = null;
    isTrackingActive = false;
    
    if (trackBtn) {
        trackBtn.innerText = "Start Tracking";
        trackBtn.classList.remove("stop-state");
        trackBtn.disabled = false;
    }
    captureBtn.disabled = false;
    timerSelect.disabled = false;
}

// Helper to start the active frame rendering loop
function startStreamingLoop() {
    clearInterval(streamIntervalId);
    isTrackingActive = true;
    
    if (trackBtn) {
        trackBtn.innerText = "Stop Tracking";
        trackBtn.classList.add("stop-state");
        trackBtn.disabled = false; // Always enabled so users can click stop manually!
    }
    captureBtn.disabled = false; 
    timerSelect.disabled = false;
    
    streamIntervalId = setInterval(streamFrame, SEND_INTERVAL_MS);
}

// Capture Button logic
captureBtn.addEventListener("click", () => {
    // Lock controls down instantly during the capture countdown phase
    captureBtn.disabled = true;
    if (trackBtn) trackBtn.disabled = true;
    timerSelect.disabled = true;

    // Read the dropdown timer value exclusively for taking a picture
    let countdownSeconds = parseInt(timerSelect.value) || 0;

    const runCountdown = () => {
        if (countdownSeconds > 0) {
            if (countdownDisplay) countdownDisplay.innerText = countdownSeconds;
            countdownSeconds--;
            setTimeout(runCountdown, 1000);
        } else {
            if (countdownDisplay) countdownDisplay.innerText = "";
            
            // 1. Terminate the active tracking stream first when photo is officially snapped
            stopStreamingLoop();
            
            // 2. Process and draw local visual confirmation capture frame
            takePhotoPreview();
        }
    };

    runCountdown();
});

function takePhotoPreview() {
    const ctx = captureCanvas.getContext("2d");
    captureCanvas.width = webcamVideo.videoWidth;
    captureCanvas.height = webcamVideo.videoHeight;
    
    if (currentFacingMode === "user") {
        ctx.translate(captureCanvas.width, 0);
        ctx.scale(-1, 1);
    }
    
    ctx.drawImage(webcamVideo, 0, 0, captureCanvas.width, captureCanvas.height);
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    
    const dataUrl = captureCanvas.toDataURL("image/jpeg");
    photoPreview.src = dataUrl;
    previewContainer.style.display = "block";
    
    // Fully clear locks on interface targets
    captureBtn.disabled = false;
    if (trackBtn) trackBtn.disabled = false;
    timerSelect.disabled = false;
}

// Tracking Button logic (FIXED: Fires instantly, completely independent of the timer dropdown)
if (trackBtn) {
    trackBtn.addEventListener("click", () => {
        if (isTrackingActive) {
            stopStreamingLoop();
            console.log("Tracking manually stopped instantly.");
        } else {
            startStreamingLoop();
            console.log("Tracking manually started instantly.");
        }
    });
}

// Initialize camera on load
startCamera(currentFacingMode);
