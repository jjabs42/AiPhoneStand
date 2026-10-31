// MADE WITH LLMS! 
// --- WEBSOCKET & TIMING PARAMETERS//
const WEBSOCKET_URL = `wss://${window.location.hostname}:5555/stream`;
const SEND_INTERVAL_MS = 2000; 
const CALIBRATION_DELAY_MS = 3000; // Time in ms to wait before sending Frame 2

const webcamVideo = document.getElementById("webcamVideo");
const flipBtn = document.getElementById("flipBtn");
const captureBtn = document.getElementById("captureBtn");
const trackBtn = document.getElementById("trackBtn"); 
const calibrateBtn = document.getElementById("calibrateBtn");
const startCalibrateBtn = document.getElementById("startCalibrateBtn");
const captureCanvas = document.getElementById("captureCanvas");
const previewContainer = document.getElementById("previewContainer");
const photoPreview = document.getElementById("photoPreview");

// UI ELEMENTS FOR TIMER & OVERLAYS
const timerSelect = document.getElementById("timerSelect"); 
const countdownDisplay = document.getElementById("countdownDisplay"); 
const calibrationOverlay = document.getElementById("calibrationOverlay");

let currentStream = null;
let currentFacingMode = "user"; 
let streamIntervalId = null; 
let isTrackingActive = false; 

// --- SETUP WEBSOCKET CLIENT ---
const socket = new WebSocket(WEBSOCKET_URL);

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

// --- WEBSOCKET INCOMING MESSAGE HANDLING ---
socket.onmessage = (event) => {
    if (typeof event.data === "string") {
        if (event.data === "CalibrationComplete" || event.data === "CalibrationDone") {
            console.log("Received calibration completion from Python server.");
            
            if (calibrationOverlay) {
                calibrationOverlay.style.display = "none";
            }
            if (startCalibrateBtn) {
                startCalibrateBtn.disabled = false;
                startCalibrateBtn.innerText = "Start";
            }
            if (calibrateBtn) {
                calibrateBtn.innerText = "Calibrate";
            }
            setControlsDisabled(false);
        }

        if (event.data === "CalibrationFailed"){
            console.log("Calibration Failed");
            setControlsDisabled(false)
            
        }
    }
        
};

// Unified UI control locker/unlocker
function setControlsDisabled(disabledState) {
    if (flipBtn) flipBtn.disabled = disabledState;
    if (captureBtn) captureBtn.disabled = disabledState;
    if (trackBtn) trackBtn.disabled = disabledState;
    if (calibrateBtn) calibrateBtn.disabled = disabledState;
    if (timerSelect) timerSelect.disabled = disabledState;
}

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

// --- AUTOMATED FRAME STREAMING FUNCTION (JSON PAYLOAD) ---
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

    // Convert canvas directly to base64 Data URL
    const base64Image = captureCanvas.toDataURL("image/jpeg", 0.6);

    const payload = JSON.stringify({
        facingMode: currentFacingMode, // "user" or "environment"
        image: base64Image
    });

    socket.send(payload);
}

// Toggle camera mode
flipBtn.addEventListener("click", () => {
    currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
    startCamera(currentFacingMode);
});

// Helper to fully clear and reset tracking loop
function stopStreamingLoop() {
    clearInterval(streamIntervalId);
    streamIntervalId = null;
    isTrackingActive = false;
    
    if (trackBtn) {
        trackBtn.innerText = "Start Tracking";
        trackBtn.classList.remove("stop-state");
    }

    if (calibrateBtn && calibrateBtn.innerText !== "Calibrating...") {
        setControlsDisabled(false);
    }
}

// Helper to start the active frame rendering loop
function startStreamingLoop() {
    clearInterval(streamIntervalId);
    isTrackingActive = true;
    
    if (trackBtn) {
        trackBtn.innerText = "Stop Tracking";
        trackBtn.classList.add("stop-state");
    }
    
    streamIntervalId = setInterval(streamFrame, SEND_INTERVAL_MS);
}

// Capture Button logic
captureBtn.addEventListener("click", () => {
    setControlsDisabled(true);

    let countdownSeconds = parseInt(timerSelect.value) || 0;

    const runCountdown = () => {
        if (countdownSeconds > 0) {
            if (countdownDisplay) countdownDisplay.innerText = countdownSeconds;
            countdownSeconds--;
            setTimeout(runCountdown, 1000);
        } else {
            if (countdownDisplay) countdownDisplay.innerText = "";
            stopStreamingLoop();
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
    
    setControlsDisabled(false);
}

// Tracking Button logic
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

// 1. Calibrate Button Logic: Shows the overlay prompt
if (calibrateBtn) {
    calibrateBtn.addEventListener("click", () => {
        if (calibrationOverlay) calibrationOverlay.style.display = "flex";
        socket.send(JSON.stringify({"CalibrationInitiated" : true}))
    });
}

// 2. Start Calibration Button Logic
if (startCalibrateBtn) {
    startCalibrateBtn.addEventListener("click", () => {
        if (socket.readyState !== WebSocket.OPEN) {
            console.error("WebSocket connection is not open.");
            return;
        }

        setControlsDisabled(true);
        startCalibrateBtn.disabled = true;
        startCalibrateBtn.innerText = "Calibrating...";
        if (calibrateBtn) calibrateBtn.innerText = "Calibrating...";

        // Step 1: Send JSON signal to Python server
        socket.send(JSON.stringify({ action: "CalibrationActive" }));
        console.log("Sent 'CalibrationActive' signal to server.");

        // Step 2: Send Frame 1 immediately
        streamFrame();
        console.log("Sent Calibration Frame 1.");

        // Step 3: Wait CALIBRATION_DELAY_MS and send Frame 2
        setTimeout(() => {
            if (socket.readyState === WebSocket.OPEN) {
                streamFrame();
                console.log(`Sent Calibration Frame 2 after ${CALIBRATION_DELAY_MS}ms.`);
            }
        }, CALIBRATION_DELAY_MS);
    });
}

// Initialize camera on load
startCamera(currentFacingMode);