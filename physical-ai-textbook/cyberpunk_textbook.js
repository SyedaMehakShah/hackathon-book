// Cyberpunk Textbook JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the wire system
    const wireSystem = document.getElementById('wireSystem');
    const textbook = document.getElementById('textbookContainer');
    const buttonContainer = document.getElementById('buttonContainer');
    const chatbotOrb = document.getElementById('chatbotOrb');
    
    // Function to draw connections between elements
    function drawConnections() {
        // Clear previous connections
        wireSystem.innerHTML = '';
        
        // Get positions of elements
        const textbookRect = textbook.getBoundingClientRect();
        const buttonRects = Array.from(buttonContainer.children).map(btn => btn.getBoundingClientRect());
        const chatbotRect = chatbotOrb.getBoundingClientRect();
        
        // Draw wires from textbook to buttons
        buttonRects.forEach(rect => {
            drawWire(
                textbookRect.left + textbookRect.width/2, 
                textbookRect.top + textbookRect.height/2,
                rect.left + rect.width/2, 
                rect.top + rect.height/2
            );
        });
        
        // Draw wire from textbook to chatbot
        drawWire(
            textbookRect.left + textbookRect.width/2, 
            textbookRect.top + textbookRect.height/2,
            chatbotRect.left + chatbotRect.width/2, 
            chatbotRect.top + chatbotRect.height/2
        );
    }
    
    // Function to draw a single wire between two points
    function drawWire(x1, y1, x2, y2) {
        const length = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
        const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;
        
        const wire = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        wire.setAttribute('x1', x1);
        wire.setAttribute('y1', y1);
        wire.setAttribute('x2', x2);
        wire.setAttribute('y2', y2);
        wire.setAttribute('stroke', 'rgba(0, 255, 255, 0.6)');
        wire.setAttribute('stroke-width', '1');
        wire.setAttribute('stroke-dasharray', '5,5');
        
        // Add animation to the wire
        const animate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        animate.setAttribute('attributeName', 'stroke');
        animate.setAttribute('values', 'rgba(0, 255, 255, 0.6);rgba(255, 0, 255, 0.8);rgba(0, 255, 255, 0.6)');
        animate.setAttribute('dur', '3s');
        animate.setAttribute('repeatCount', 'indefinite');
        
        wire.appendChild(animate);
        wireSystem.appendChild(wire);
    }
    
    // Initial draw
    drawConnections();
    
    // Redraw connections when window resizes
    window.addEventListener('resize', drawConnections);
    
    // Add hover effect to highlight connections
    const buttons = document.querySelectorAll('.glass-button');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            highlightConnection(textbook, button);
        });
        
        button.addEventListener('mouseleave', () => {
            drawConnections(); // Reset to default
        });
    });
    
    // Highlight connection between two elements
    function highlightConnection(el1, el2) {
        wireSystem.innerHTML = '';
        
        const rect1 = el1.getBoundingClientRect();
        const rect2 = el2.getBoundingClientRect();
        
        const wire = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        wire.setAttribute('x1', rect1.left + rect1.width/2);
        wire.setAttribute('y1', rect1.top + rect1.height/2);
        wire.setAttribute('x2', rect2.left + rect2.width/2);
        wire.setAttribute('y2', rect2.top + rect2.height/2);
        wire.setAttribute('stroke', 'rgba(255, 0, 255, 0.9)');
        wire.setAttribute('stroke-width', '2');
        wire.setAttribute('stroke-dasharray', '5,5');
        
        // Add pulse animation
        const animate = document.createElementNS('http://www.w3.org/2000/svg', 'animate');
        animate.setAttribute('attributeName', 'stroke');
        animate.setAttribute('values', 'rgba(255, 0, 255, 0.9);rgba(0, 255, 255, 0.9);rgba(255, 0, 255, 0.9)');
        animate.setAttribute('dur', '1s');
        animate.setAttribute('repeatCount', 'indefinite');
        
        wire.appendChild(animate);
        wireSystem.appendChild(wire);
    }
    
    // Create floating particles in the background
    function createParticles() {
        const particlesContainer = document.querySelector('.particles');
        
        for (let i = 0; i < 50; i++) {
            const particle = document.createElement('div');
            particle.classList.add('particle');
            
            // Random position
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            
            // Random size
            const size = Math.random() * 3 + 1;
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            
            // Random animation duration
            const duration = Math.random() * 20 + 10;
            particle.style.animationDuration = `${duration}s`;
            
            // Random destination for animation
            const targetX = (Math.random() - 0.5) * 100;
            const targetY = (Math.random() - 0.5) * 100;
            particle.style.setProperty('--target-x', `${targetX}vw`);
            particle.style.setProperty('--target-y', `${targetY}vh`);
            
            particlesContainer.appendChild(particle);
        }
    }
    
    // Position floating code snippets randomly
    function positionCodeSnippets() {
        const codeSnippets = document.querySelectorAll('.code-snippet');
        
        codeSnippets.forEach(snippet => {
            // Random position
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            snippet.style.left = `${posX}%`;
            snippet.style.top = `${posY}%`;
            
            // Random delay and duration
            const delay = Math.random() * 15;
            const duration = Math.random() * 10 + 15;
            snippet.style.animationDelay = `${delay}s`;
            snippet.style.animationDuration = `${duration}s`;
        });
    }
    
    // Initialize particles and code snippets
    createParticles();
    positionCodeSnippets();
    
    // Add glowing cursor effect
    const cursorGlow = document.getElementById('cursorGlow');
    document.body.addEventListener('mousemove', (e) => {
        cursorGlow.style.display = 'block';
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });
    
    document.body.addEventListener('mouseleave', () => {
        cursorGlow.style.display = 'none';
    });
    
    // Book interaction - slightly opens on hover
    const textbookElement = document.getElementById('textbook');
    textbookElement.addEventListener('mouseenter', () => {
        textbookElement.style.transform = 'translateY(-15px) rotateX(10deg) rotateY(10deg) scale(1.05)';
    });
    
    textbookElement.addEventListener('mouseleave', () => {
        textbookElement.style.transform = 'translateY(-15px) rotateX(5deg) rotateY(5deg) scale(1.05)';
    });
    
    // Button click effects
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size/2;
            const y = e.clientY - rect.top - size/2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: radial-gradient(circle, rgba(0,255,255,0.6) 0%, transparent 70%);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
                z-index: 0;
            `;
            
            this.appendChild(ripple);
            
            // Remove ripple after animation completes
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add ripple animation to CSS dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Chatbot orb interaction
    const chatbotOrbElement = document.getElementById('chatbotOrb');
    const chatInterface = document.getElementById('chatInterface');
    const closeChat = document.getElementById('closeChat');
    
    chatbotOrbElement.addEventListener('click', () => {
        chatInterface.style.display = 'flex';
    });
    
    closeChat.addEventListener('click', () => {
        chatInterface.style.display = 'none';
    });
    
    // Read Textbook button functionality
    const readButton = document.getElementById('readButton');

    readButton.addEventListener('click', () => {
        // Open the textbook intro page in the same window
        window.location.href = '/docs/intro';

        // Provide instructions to the user
        const instructions = 'If the textbook did not open, please run "npm run start" in the physical-ai-textbook directory first.\n\nIn your terminal, navigate to the physical-ai-textbook directory and run:\nnpm run start';
        console.log(instructions); // Log to console as an alternative to alert
        // alert(instructions); // Uncomment this line if you want to show an alert
    });

    // Chat functionality
    const sendButton = document.getElementById('sendButton');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message
            const userMsgElement = document.createElement('div');
            userMsgElement.classList.add('message', 'user-message');
            userMsgElement.textContent = message;
            chatMessages.appendChild(userMsgElement);

            // Clear input
            userInput.value = '';

            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Simulate AI response after a delay
            setTimeout(() => {
                const aiResponse = generateAIResponse(message);
                const aiMsgElement = document.createElement('div');
                aiMsgElement.classList.add('message', 'ai-message');
                aiMsgElement.textContent = aiResponse;
                chatMessages.appendChild(aiMsgElement);

                // Scroll to bottom again
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 1000);
        }
    }

    function generateAIResponse(userMessage) {
        // Simple response generation - in a real app this would connect to an AI API
        const responses = [
            "That's an interesting concept from the textbook. The neural network architecture builds on these foundational principles.",
            "Based on the chapter on machine learning, this topic connects to several important algorithms.",
            "The textbook explains this concept in detail in Chapter 4. Would you like me to elaborate?",
            "This is a key principle in AI development. The mathematical foundation is quite elegant.",
            "I found relevant information in the textbook. This concept is fundamental to understanding AI systems."
        ];

        return responses[Math.floor(Math.random() * responses.length)];
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Initial connections draw after DOM is fully loaded
    setTimeout(drawConnections, 100);
});