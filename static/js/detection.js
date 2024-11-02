let detectionInterval;
let speakInterval;
let isDetecting = false;
let lastDetectionText = ''; // Keep track of the last detected text

function startDetection() {
    if (!isDetecting) {
        isDetecting = true;
        updateDetections();
        detectionInterval = setInterval(updateDetections, 2000);
        document.getElementById("start-btn").disabled = true;
        document.getElementById("stop-btn").disabled = false;
    }
}

function stopDetection() {
    if (isDetecting) {
        isDetecting = false;
        clearInterval(detectionInterval);
        clearInterval(speakInterval);
        document.getElementById("stop-btn").disabled = true;
        document.getElementById("start-btn").disabled = false;
        document.getElementById("current-detection").value = '';
        document.getElementById("detection-log").value = '';
    }
}

function updateDetections() {
    fetch('/get_detections')
        .then(response => response.json())
        .then(data => {
            const currentDetectionArea = document.getElementById('current-detection');
            const newDetectionText = data.current_detection || 'No current detection.';
            currentDetectionArea.value = newDetectionText;

            const detectionLogArea = document.getElementById('detection-log');
            detectionLogArea.value = '';
            if (data.detection_log && data.detection_log.length > 0) {
                data.detection_log.forEach(item => {
                    detectionLogArea.value += item + '\n';
                });
            } else {
                detectionLogArea.value = 'No detections logged.\n';
            }

            // Only trigger speak detection if the text has changed
            if (newDetectionText !== lastDetectionText) {
                lastDetectionText = newDetectionText;
                speakDetection(); // Call speakDetection whenever there's new text
            }
        })
        .catch(error => console.error('Error fetching detections:', error));
}

function speakDetection() {
    const detectionText = document.getElementById('current-detection').value;
    if (!detectionText) {
        console.warn("No detection text available to speak.");
        return;
    }

    const apiKey = "NFSlr2Ojxg0bQME9czvGCKY1v980vEgY"; // Replace with your actual API key
    const requestData = {
        model: "tts-1",
        input: detectionText,
        voice: "alloy"
    };

    fetch("https://api.on-demand.io/services/v1/public/service/execute/text_to_speech", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "apikey": apiKey
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.data && data.data.audioUrl) {
            const audio = new Audio(data.data.audioUrl);
            audio.play();
        } else {
            console.error("Error with response data:", data);
        }
    })
    .catch(error => console.error("Error converting text to speech:", error));
}

// Event Listeners
document.getElementById("start-btn").addEventListener("click", startDetection);
document.getElementById("stop-btn").addEventListener("click", stopDetection);

// Continuous speak detection on button click
document.getElementById("speak-btn").addEventListener("click", () => {
    lastDetectionText = ''; // Reset last detection text to trigger reading on any update
    speakInterval = setInterval(speakDetection, 2000); // Call speakDetection every 2 seconds
});
