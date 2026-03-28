function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));
    
    // Show the selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Add active class to the clicked tab button
    event.target.classList.add('active');
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const message = input.value.trim();
    
    if (message) {
        // Add user message
        const userMessage = document.createElement('div');
        userMessage.textContent = 'You: ' + message;
        messages.appendChild(userMessage);
        
        // Show loading
        const loadingMessage = document.createElement('div');
        loadingMessage.textContent = 'NASA Bot: Thinking...';
        loadingMessage.id = 'loading';
        messages.appendChild(loadingMessage);
        
        // Scroll to bottom
        messages.scrollTop = messages.scrollHeight;
        
        // Send to API
        fetch('http://localhost:8001/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading
            document.getElementById('loading').remove();
            
            // Add bot response
            const botMessage = document.createElement('div');
            botMessage.textContent = 'NASA Bot: ' + (data.answer || 'Sorry, I couldn\'t process that question.');
            messages.appendChild(botMessage);
            
            // Scroll to bottom
            messages.scrollTop = messages.scrollHeight;
        })
        .catch(error => {
            // Remove loading
            if (document.getElementById('loading')) {
                document.getElementById('loading').remove();
            }
            
            // Add error message
            const errorMessage = document.createElement('div');
            errorMessage.textContent = 'NASA Bot: Error connecting to server. Please make sure the RAG API is running.';
            messages.appendChild(errorMessage);
            
            // Scroll to bottom
            messages.scrollTop = messages.scrollHeight;
        });
        
        // Clear input
        input.value = '';
    }
}

function submitQuestion() {
    const questionInput = document.getElementById('question-input');
    const feedback = document.getElementById('question-feedback');
    const text = questionInput.value.trim();

    if (!text) {
        feedback.textContent = 'Please enter a question before submitting.';
        feedback.style.color = 'red';
        return;
    }

    feedback.style.color = '#2f6e2f';
    feedback.textContent = `Question submitted: "${text}". An instructor will respond shortly.`;
    questionInput.value = '';
}