function showMessage(message) {
            document.getElementById("message").innerText = message;
            document.getElementById("message-container").style.display = "block";
        }

        document.addEventListener("DOMContentLoaded", function() {
            document.querySelector(".new-button2").addEventListener("click", function(event) {
                event.preventDefault();
                const url = event.target.parentElement.getAttribute("href");

                fetch(url)
                    .then(response => {
                        if (response.ok) {
                            return response.blob();
                        } else {
                            throw new Error("No Solution Found!");
                        }
                    })
                    .then(blob => {
                        const downloadUrl = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.style.display = 'none';
                        a.href = downloadUrl;
                        a.download = 'solution.pdf';  // Modify this according to your file type and name
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(downloadUrl);
                    })
                    .catch(error => {
                        alert(error.message);
                    });
            });
        });