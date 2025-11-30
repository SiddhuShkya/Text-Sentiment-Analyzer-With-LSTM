document.addEventListener('DOMContentLoaded', () => {
    const textInput = document.getElementById('textInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const sentimentBadge = document.getElementById('sentimentBadge');
    const sentimentIcon = document.getElementById('sentimentIcon');
    const sentimentLabel = document.getElementById('sentimentLabel');
    const barsContainer = document.getElementById('barsContainer');

    let confidenceChart = null;

    analyzeBtn.addEventListener('click', async () => {
        const text = textInput.value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        // UI State: Loading
        analyzeBtn.disabled = true;
        loadingSpinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) throw new Error('Analysis failed');

            const data = await response.json();
            updateUI(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis. Please try again.');
        } finally {
            analyzeBtn.disabled = false;
            loadingSpinner.classList.add('hidden');
        }
    });

    function updateUI(data) {
        const { sentiment, probabilities } = data;

        // Update Badge
        sentimentBadge.className = `badge ${sentiment}`;
        sentimentLabel.textContent = sentiment;

        const icons = {
            positive: '<i class="fa-solid fa-face-smile"></i>',
            negative: '<i class="fa-solid fa-face-frown"></i>',
            neutral: '<i class="fa-solid fa-face-meh"></i>'
        };
        sentimentIcon.innerHTML = icons[sentiment];

        // Update Chart
        updateChart(probabilities);

        // Update Progress Bars
        updateBars(probabilities);

        // Show Results
        resultsSection.classList.remove('hidden');
    }

    function updateChart(probs) {
        const ctx = document.getElementById('confidenceChart').getContext('2d');

        const dataValues = [probs.positive, probs.neutral, probs.negative];
        const labels = ['Positive', 'Neutral', 'Negative'];
        const colors = ['#22c55e', '#64748b', '#ef4444'];

        if (confidenceChart) {
            confidenceChart.destroy();
        }

        confidenceChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: dataValues,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Inter' }
                        }
                    }
                }
            }
        });
    }

    function updateBars(probs) {
        barsContainer.innerHTML = '';

        const items = [
            { label: 'Positive', value: probs.positive, color: '#22c55e' },
            { label: 'Neutral', value: probs.neutral, color: '#64748b' },
            { label: 'Negative', value: probs.negative, color: '#ef4444' }
        ];

        items.forEach(item => {
            const percentage = (item.value * 100).toFixed(1);
            const html = `
                <div class="bar-item">
                    <div class="bar-label">
                        <span>${item.label}</span>
                        <span>${percentage}%</span>
                    </div>
                    <div class="progress-bg">
                        <div class="progress-fill" style="width: ${percentage}%; background-color: ${item.color}"></div>
                    </div>
                </div>
            `;
            barsContainer.insertAdjacentHTML('beforeend', html);
        });
    }
});
