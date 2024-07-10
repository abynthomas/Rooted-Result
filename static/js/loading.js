document.addEventListener("DOMContentLoaded", function() {
            // Show loading GIF
    document.getElementById('loading').style.display = 'block';
            // Hide loading GIF after 2 seconds
    setTimeout(function() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('main-content').style.display = 'block';
    }, 2000);
});
