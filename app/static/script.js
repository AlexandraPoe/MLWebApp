async function predictRegression() {
    const formData = new FormData(document.getElementById("inputForm"));
    const data = Object.fromEntries(formData.entries());
    console.log("Payload to server:", data); // Debug log
    const response = await fetch("/predict_regression", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    console.log("Response from server:", result); // Debug log
    document.getElementById("regressionResult").innerText = `ERP Prediction: ${result["ERP Prediction"]}`;
}

    async function predictClassification() {
    try {
    const formData = new FormData(document.getElementById("inputForm"));
    const data = Object.fromEntries(formData.entries());
    const response = await fetch("/predict_classification", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data),
});

    if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
}

    const result = await response.json();
    document.getElementById("classificationResult").innerText = result["Performance Prediction"] || "No result returned";
} catch (error) {
    console.error("Error during classification prediction:", error);
    document.getElementById("classificationResult").innerText = "Error occurred during prediction.";
}
}
