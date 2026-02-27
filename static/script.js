document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('generator-form');
    const promptInput = document.getElementById('prompt-input');
    const tags = document.querySelectorAll('.tag');

    // State Containers
    const loadingState = document.getElementById('loading-state');
    const errorState = document.getElementById('error-state');
    const resultState = document.getElementById('result-state');
    const errorMessage = document.getElementById('error-message');

    // Result Elements
    const circuitImage = document.getElementById('circuit-image');
    const circuitTypeLabel = document.getElementById('circuit-type-label');
    const circuitDescription = document.getElementById('circuit-description');
    const circuitVerification = document.getElementById('circuit-verification');

    // Handle Quick Tags
    tags.forEach(tag => {
        tag.addEventListener('click', () => {
            promptInput.value = tag.getAttribute('data-prompt');
            // Add a little visual flair
            tag.style.transform = 'scale(0.95)';
            setTimeout(() => tag.style.transform = 'scale(1)', 150);
        });
    });

    // Handle Form Submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const promptText = promptInput.value.trim();
        if (!promptText) return;

        // UI State: Loading
        hideAllStates();
        loadingState.classList.remove('hidden');

        try {
            const response = await fetch('https://shashank-a-n-ai-circuit.hf.space/api/generate_circuit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: promptText })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Failed to generate circuit. Server anomaly detected.');
            }

            // UI State: Success
            hideAllStates();

            // We remove the strict await imgLoadPromise here.
            // Just set the src and let it load asynchronously without blocking the UI reveal.
            // This prevents the 'AbortError: The play() request was interrupted' if a new request is made quickly.

            // Prevent caching issues by appending timestamp if needed, but Flask handles this generally
            circuitImage.src = data.image_url;
            circuitTypeLabel.textContent = data.circuit_type;
            circuitDescription.textContent = data.description;
            circuitVerification.textContent = data.verification;

            const filename = data.image_url.split('/').pop();
            const editBtn = document.getElementById('edit-circuit-btn');
            const dlBtn = document.getElementById('download-circuit-btn');

            if (editBtn) {
                editBtn.href = `editor.html?image=${filename}`;
                editBtn.target = '_self'; // Directly transfer without opening a new tab
            }
            if (dlBtn) {
                dlBtn.href = data.image_url;
                dlBtn.download = filename;
            }

            resultState.classList.remove('hidden');

            // Scroll to results softly
            resultState.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (error) {
            // UI State: Error
            hideAllStates();
            errorMessage.textContent = error.message;
            errorState.classList.remove('hidden');
        }
    });

    function hideAllStates() {
        loadingState.classList.add('hidden');
        errorState.classList.add('hidden');
        resultState.classList.add('hidden');
    }
});


