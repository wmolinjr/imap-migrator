/**
 * Terminal-like functionality for log viewer
 * Handles auto-scrolling to keep the latest content visible
 */

// Function to scroll to bottom
function scrollToBottom() {
    // Try multiple methods to ensure scrolling works in all browsers
    window.scrollTo(0, document.body.scrollHeight);
    document.documentElement.scrollTop = document.documentElement.scrollHeight;

    // If we're in an iframe, also try to scroll the parent
    if (window.parent && window.parent !== window) {
        try {
            window.parent.document.getElementById('log-container').scrollTop = 
                window.parent.document.getElementById('log-container').scrollHeight;
        } catch(e) {
            // Ignore errors from cross-origin restrictions
        }
    }
}

// Scroll on load
window.onload = scrollToBottom;

// Also scroll after a short delay to handle any dynamic content
setTimeout(scrollToBottom, 100);