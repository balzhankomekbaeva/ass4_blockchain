        document.addEventListener('DOMContentLoaded', () => {
            const chatHistory = document.getElementById('chat-history');
            const userInput = document.getElementById('user-input');
            const sendButton = document.getElementById('send-button');
            const queryCards = document.querySelectorAll('.query-card');
            const ollamaStatus = document.getElementById('ollama-status');
            const modelSelect = document.getElementById('model-select');
            const modelSelection = document.getElementById('model-selection');

            // Check system status
            checkStatus();

            // Add event listeners
            sendButton.addEventListener('click', sendMessage);
            userInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            queryCards.forEach(card => {
                card.addEventListener('click', () => {
                    const query = card.getAttribute('data-query');
                    if (query) {
                        userInput.value = query;
                        sendMessage();
                    }
                });
            });

            // Check status of services
            function checkStatus() {
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        // Update Ollama status
                        const statusClass = data.ollama ? 'status-online' : 'status-offline';
                        const statusText = data.ollama ? 'Online' : 'Offline';
                        
                        ollamaStatus.innerHTML = `
                            <span class="status-indicator ${statusClass}"></span>${statusText}
                        `;

                        // If Ollama is online, populate model selection
                        if (data.ollama && data.models && data.models.length > 0) {
                            modelSelection.classList.remove('d-none');
                            
                            // Clear existing options
                            modelSelect.innerHTML = '';
                            
                            // Add available models
                            data.models.forEach(model => {
                                const option = document.createElement('option');
                                option.value = model;
                                option.textContent = model;
                                
                                // Set current model as selected
                                if (model === data.current_model) {
                                    option.selected = true;
                                }
                                
                                modelSelect.appendChild(option);
                            });
                            
                            // Add event listener to model select
                            modelSelect.addEventListener('change', () => {
                                const selectedModel = modelSelect.value;
                                changeModel(selectedModel);
                            });
                        } else {
                            modelSelection.classList.add('d-none');
                        }
                    })
                    .catch(error => {
                        console.error('Error checking status:', error);
                        ollamaStatus.innerHTML = `
                            <span class="status-indicator status-offline"></span>Error
                        `;
                    });
            }

            // Change the model
            function changeModel(model) {
                fetch('/api/set_model', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ model })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        addMessage('System', `Changed model to ${model}`, 'assistant-message');
                    } else {
                        addMessage('System', `Failed to change model: ${data.error}`, 'assistant-message');
                    }
                })
                .catch(error => {
                    console.error('Error changing model:', error);
                    addMessage('System', 'Failed to change model due to an error', 'assistant-message');
                });
            }

            function sendMessage() {
                const message = userInput.value.trim();
                if (!message) return;

                // Add user message to chat
                addMessage('You', message, 'user-message');
                userInput.value = '';

                // Show thinking indicator
                const thinkingMsg = addMessage('AI', 'Thinking...', 'assistant-message');

                // Send request to server
                fetch('/api/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: message })
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server responded with ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Remove thinking message
                    chatHistory.removeChild(thinkingMsg);
                    
                    // Add assistant response
                    addMessage('AI', data.response, 'assistant-message');
                })
                .catch(error => {
                    // Remove thinking message
                    chatHistory.removeChild(thinkingMsg);
                    
                    console.error('Error:', error);
                    const errorMessage = error.message.includes('Failed to fetch') ? 
                        'Server is not responding. Please check if the server is running.' :
                        `Error: ${error.message}`;
                    
                    addMessage('System', errorMessage, 'assistant-message');
                });
            }

            function addMessage(sender, text, className) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${className}`;
                
                const senderSpan = document.createElement('strong');
                senderSpan.textContent = sender + ': ';
                
                const textSpan = document.createElement('span');
                textSpan.textContent = text;
                
                messageDiv.appendChild(senderSpan);
                messageDiv.appendChild(textSpan);
                
                chatHistory.appendChild(messageDiv);
                
                // Auto scroll to bottom
                chatHistory.scrollTop = chatHistory.scrollHeight;
                
                return messageDiv;
            }
        });