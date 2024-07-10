  document.addEventListener('DOMContentLoaded', function() {
    // Get all table cells
    var cells = document.querySelectorAll('tbody td');

    // Loop through each cell
    cells.forEach(function(cell) {
      // Check if cell content is NaN
      if (isNaN(parseFloat(cell.textContent))) {
        // Replace NaN with '-'
        cell.textContent = '-';
      }
    });
  });