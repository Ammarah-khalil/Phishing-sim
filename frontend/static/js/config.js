// Replace this with your actual Railway Backend URL after deployment
// Example: const API_BASE_URL = "https://phishing-sim-production.up.railway.app";
const API_BASE_URL = "http://localhost:5000"; // Default for local testing works if not cross-origin, but for GH pages needs real URL.

// Helper to update form actions
document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const action = form.getAttribute('action');
        // Only modify if it's a relative path starting with /
        if (action && action.startsWith('/')) {
            form.action = API_BASE_URL + action;
            console.log("Updated form action to:", form.action);
        }
    });
});
