// Get references to the camera view and capture button
const cameraView = document.getElementById("camera-view");
const captureButton = document.getElementById("capture-button");

// Start the camera stream when the page loads
window.addEventListener("load", () => {
  // Get the user's camera stream
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      // Display the camera view in the video element
        cameraView.srcObject = stream;
        cameraView.play();
    })
    .catch(error => {
      console.error("Failed to get camera stream", error);
    });
});

// Add an event listener to the capture button
captureButton.addEventListener("click", () => {
  // Create a canvas element to capture the image
  const canvas = document.createElement("canvas");
  canvas.width = cameraView.videoWidth;
  canvas.height = cameraView.videoHeight;

  // Draw the camera view onto the canvas
  const context = canvas.getContext("2d");
  context.drawImage(cameraView, 0, 0, canvas.width, canvas.height);

  // Convert the canvas to a data URL
  const dataUrl = canvas.toDataURL("image/png");

  // Send the data URL to the server for prediction
  fetch("/predict", {
    method: "POST",
    body: JSON.stringify({ image: dataUrl }),
    headers: { "Content-Type": "application/json" }
  })
  .then(response => response.json())
  .then(result => {
    // Display the predicted label in the result div
    const resultDiv = document.getElementById("result");
    resultDiv.innerText = `Predicted label: ${result.label}`;
  })
  .catch(error => {
    console.error("Failed to make prediction", error);
  });
});
