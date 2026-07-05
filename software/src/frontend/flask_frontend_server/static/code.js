
// --- WEBSOCKET & TIMING PARAMETERS, Created with llms ---
const WEBSOCKET_URL = "ws://localhost:5555/stream"; 
const SEND_INTERVAL_MS = 2000; // Change this number! (2000ms = every 2 seconds)

const webcamVideo = document.getElementById("webcamVideo");
const flipBtn = document.getElementById("flipBtn");
const captureBtn = document.getElementById("captureBtn");
const captureCanvas = document.getElementById("captureCanvas");
const previewContainer = document.getElementById("previewContainer");
const photoPreview = document.getElementById("photoPreview");

let currentStream = null;
let currentFacingMode = "user"; 

// --- SETUP WEBSOCKET CLIENT ---
const socket = new WebSocket(WEBSOCKET_URL);
socket.binaryType = 'arraybuffer'; // Tells browser to pass raw data out of RAM

socket.onopen = () => {
    console.log("Connected to Python Server!");
    // Start the automated loop once the connection establishes
    setInterval(streamFrame, SEND_INTERVAL_MS);
};

socket.onerror = (error) => {
    console.error("WebSocket Error: ", error);
};

socket.onclose = () => {
    console.log("Disconnected from Python Server.");
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
    // 1. Must have active WebSocket
    if (socket.readyState !== WebSocket.OPEN) {
        console.log("Socket not ready");
        return;
    }

    // 2. Must have valid camera frame
    if (!webcamVideo.videoWidth || !webcamVideo.videoHeight) {
        console.log("Video not ready");
        return;
    }

    const ctx = captureCanvas.getContext("2d");

    // 3. Always reset transforms first (IMPORTANT)
    ctx.setTransform(1, 0, 0, 1, 0, 0);

    // 4. Match canvas to video size
    captureCanvas.width = webcamVideo.videoWidth;
    captureCanvas.height = webcamVideo.videoHeight;

    // 5. Optional mirror for front camera
    if (currentFacingMode === "user") {
        ctx.translate(captureCanvas.width, 0);
        ctx.scale(-1, 1);
    }

    // 6. Draw current frame
    ctx.drawImage(webcamVideo, 0, 0, captureCanvas.width, captureCanvas.height);

    // 7. Encode and send
    captureCanvas.toBlob((blob) => {
        if (!blob) {
            console.log("toBlob failed");
            return;
        }

        if (socket.readyState !== WebSocket.OPEN) return;

        socket.send(blob);
        console.log("Sent frame:", blob.size, "bytes");

    }, "image/jpeg", 0.85); // good balance of quality + speed
}

// Toggle camera mode
flipBtn.addEventListener("click", () => {
    currentFacingMode = currentFacingMode === "user" ? "environment" : "user";
    startCamera(currentFacingMode);
});

// Manual Capture Button Action (Kept intact)
captureBtn.addEventListener("click", () => {
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
});

// Initialize camera on load
startCamera(currentFacingMode);
