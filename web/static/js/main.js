// Main JavaScript for Melbourne AI Web UI

// Log initialization
console.log('Melbourne AI Video Creator initialized');

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add loading animation to buttons
function addButtonLoader(button) {
    button.classList.add('loading');
    button.disabled = true;
}

function removeButtonLoader(button) {
    button.classList.remove('loading');
    button.disabled = false;
}

// Format time
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

// API Helper
class API {
    static async request(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const response = await fetch(endpoint, { ...defaultOptions, ...options });
        return response.json();
    }

    static async get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }

    static async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }
}

// Analytics (optional)
function trackEvent(eventName, eventData = {}) {
    console.log(`Event: ${eventName}`, eventData);
    // Can be extended to send to analytics service
}

// Export for use in other scripts
window.API = API;
window.trackEvent = trackEvent;
window.formatTime = formatTime;
