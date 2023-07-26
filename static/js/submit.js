document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('submit-button');
    const userInput = document.getElementById('user-input');
    const errorText = document.getElementById('error-text');
    const resultsDiv = document.getElementById('compare-results');
    let originalSentence = document.getElementById('sentence').textContent; // Get the original sentence
    console.log("Original Sentence: ", originalSentence.trim());
    submitButton.addEventListener('click', function () {
        // Reset error text
        errorText.textContent = '';

        // Validate input
        if (userInput.value.trim() === '') {
            errorText.textContent = 'Please enter your translation before submitting.';
            return;
        }

        if (submitButton.textContent === 'Next') {
            // Fetch new sentence and update originalSentence
            fetch('/next_sentence/')
                .then(response => response.text())
                .then(data => {
                    const parser = new DOMParser();
                    const htmlDocument = parser.parseFromString(data, "text/html");
                    const newSentence = htmlDocument.getElementById('sentence').textContent;
                    const newTranslation = htmlDocument.getElementById('translation').textContent;  // get the new translation

                    originalSentence = newSentence;  // update the original sentence

                    document.getElementById('sentence').textContent = newSentence;
                    document.getElementById('translation').textContent = newTranslation;  // update the translation

                    // Reset resultsDiv and userInput
                    resultsDiv.innerHTML = '';
                    userInput.value = '';

                    // Change the button text to 'Submit'
                    submitButton.textContent = 'Submit';
                });

            return;
        }


        // If the button says 'Submit', send a POST request to the compare endpoint
        fetch('compare/', {
            method: 'POST',
            body: JSON.stringify({
                user_sentence: userInput.value,
                original_sentence: originalSentence,
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        })
            .then(response => response.json())
            .then(data => {
                // Display the results in a user-friendly way
                resultsDiv.innerHTML = `
                    <h2>Results</h2>
                    <p>Overall similarity score: ${data.similarity}</p>
                    <p>Your sentence: ${userInput.textContent}</p>
                `;

                data.word_scores.forEach(([word, score]) => {
                    resultsDiv.innerHTML += `<p>${word}: ${score}</p>`;
                });

                // Change the button text to 'Next'
                submitButton.textContent = 'Next';
            });

    });
});
