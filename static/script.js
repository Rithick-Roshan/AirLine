document.addEventListener("DOMContentLoaded", function() {
    // Handle login form submission
    document.getElementById("login-form").addEventListener("submit", function(event) {
        event.preventDefault();
        
        var form = event.target;
        var formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            showError("An error occurred. Please try again.");
            console.error('Error:', error);
        });
    });

    // Handle signup form submission
    document.getElementById("signup-form").addEventListener("submit", function(event) {
        event.preventDefault();
        
        var form = event.target;
        var formData = new FormData(form);

        fetch(form.action, {
            method: form.method,
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.redirect_url;
            } else {
                showError(data.error);
            }
        })
        .catch(error => {
            showError("An error occurred. Please try again.");
            console.error('Error:', error);
        });
    });

    // Function to show error messages with animation
    function showError(message) {
        var errorMessage = document.getElementById("error-message");
        errorMessage.innerText = message;
        errorMessage.style.opacity = 0;
        errorMessage.style.display = "block";
        fadeIn(errorMessage, 500);
    }

    // Fade-in animation function
    function fadeIn(element, duration) {
        var opacity = 0;
        var interval = 50;
        var gap = interval / duration;

        function increase() {
            opacity += gap;
            if (opacity <= 1) {
                element.style.opacity = opacity;
                requestAnimationFrame(increase);
            }
        }
        increase();
    }
});
