document.addEventListener("DOMContentLoaded", function () {
    const recordBtn = document.getElementById("recordBtn");
    let recording = false; // 🔹 Track recording state

    recordBtn.addEventListener("click", async () => {
        if (!recording) {
            recording = true;
            recordBtn.textContent = "🛑 Stop Recording";
            
            // 🎤 Start recording
            fetch("/record/")
                .then(response => response.json())
                .then(data => {
                    console.log("🎙️ Recording started...");
                })
                .catch(error => console.error("❌ Error starting recording:", error));
            } else {
                recording = false;
                recordBtn.textContent = "🎤 Start Recording";
                
                fetch("/stop_record/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({ audio_file: filename }) // ✅ send audio_file clearly
                })
                .then(response => response.json())
                .then(data => {
                    console.log("🛑 Recording stopped, transcription:", data.transcription);
                    const textBox = document.getElementById("transcribedText");
                    if (textBox && data.transcription) {
                        textBox.innerText = data.transcription; 
                    }
                })
                .catch(error => console.error("❌ Error stopping recording:", error));
            }
    });

    // 📝 Transcribe audio
    function transcribeAudio(filename) {
        const cleanFilename = filename.replace("recordings/", "");
        fetch(`/transcribe/?audio=${cleanFilename}`)
            .then(response => response.json())
            .then(data => {
                if (data.transcription) {
                    console.log("📝 Transcription:", data.transcription);
                    const textBox = document.getElementById("transcribedText");
                    if (textBox) {
                        textBox.innerText = data.transcription;  // ✅ Update UI block
                    } else {
                        console.error("❌ Element #transcribedText not found.");
                    }
                } else {
                    console.error("❌ Transcription failed:", data.error);
                }
            })
            .catch(error => console.error("❌ Error fetching transcription:", error));
    }
});