const predictionForm = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const resultDiv = document.getElementById('result');
const predictionValue = document.getElementById('predictionValue');

async function makePrediction() {
    const originalText = 'PREDICT';
    if (submitBtn.textContent !== 'CALCULATING...') {
        submitBtn.textContent = 'CALCULATING...';
        submitBtn.disabled = true;
    }

    const formData = new FormData(predictionForm);
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            predictionValue.textContent = result.prediction.toFixed(2);
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = 'rgba(255, 255, 255, 0.15)';
            resultDiv.style.color = 'white';
        } else {
            predictionValue.textContent = "Error: " + result.error;
            resultDiv.style.display = 'block';
            resultDiv.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
            resultDiv.style.color = '#ffcccb';
        }
    } catch (error) {
        console.error('Network Error:', error);
        alert('An error occurred while making prediction.');
    } finally {
        submitBtn.textContent = 'PREDICT';
        submitBtn.disabled = false;
    }
}

predictionForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    makePrediction();
});

document.getElementById('resetBtn').addEventListener('click', function () {
    predictionForm.reset();
    resultDiv.style.display = 'none';
    submitBtn.textContent = 'PREDICT';
    submitBtn.disabled = false;
});
