// Function to generate text profile picture with random colors
function generateProfilePicture() {
    // Get the full name from the input field
    var fullName = document.getElementById('name').value;

    // Extract the first and last names
    var nameParts = fullName.split(" ");
    var firstName = nameParts[0];
    var lastName = nameParts[nameParts.length - 1];

    // Get the first letters of the first name and last name
    var firstLetter = firstName.charAt(0).toUpperCase();
    var secondLetter = lastName.charAt(0).toUpperCase();

    // Create an empty canvas element
    var canvas = document.createElement('canvas');
    canvas.width = 150; // Set the width
    canvas.height = 150; // Set the height

    // Get the 2D context of the canvas
    var ctx = canvas.getContext('2d');

    // Generate random background color
    var bgColor = '#' + Math.floor(Math.random()*16777215).toString(16);

    // Draw a rectangle with random background color
    ctx.fillStyle = bgColor; // Set the background color
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Draw the rectangle

    // Generate random text color
    var textColor = '#' + Math.floor(Math.random()*16777215).toString(16);

    // Draw the initials with random text color
    ctx.fillStyle = textColor; // Set the text color
    ctx.font = 'bold 60px Arial'; // Set the font
    ctx.textAlign = 'center'; // Set the text alignment
    ctx.fillText(firstLetter + secondLetter, canvas.width / 2, canvas.height / 2 + 20); // Draw the initials

    // Convert the canvas to a data URL
    var dataURL = canvas.toDataURL();

    // Log the generated dataURL to the console
    console.log('Generated dataURL:', dataURL);

    // Set the data URL as the background image of the profile photo container
    document.getElementById('profilePhotoContainer').style.backgroundImage = 'url(' + dataURL + ')';

    // Set the same data URL as the background image of the navbar profile picture
    document.getElementById('navbarProfilePicture').style.backgroundImage = 'url(' + dataURL + ')';
}

// Function to format the phone number to display only the last 10 digits
function formatPhoneNumber(phoneNumber) {
    // Remove all non-numeric characters from the phone number
    var numericPhoneNumber = phoneNumber.replace(/\D/g, '');

    // Extract the last 10 digits
    var lastTenDigits = numericPhoneNumber.slice(-10);

    return lastTenDigits;
}

// Call the functions when the page loads
window.onload = function() {
    // Generate the profile picture
    generateProfilePicture();

    // Get the phone number input field
    var phoneInput = document.getElementById('phone');

    // Get the current phone number value
    var phoneNumber = phoneInput.value;

    // Format the phone number and update the input field
    phoneInput.value = formatPhoneNumber(phoneNumber);
};