function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.autoTable({
      html: '#activity-table',
      theme: 'grid',
      styles: {
        halign: 'center'
      }
    });

    doc.save('Student_Activity_Details.pdf');
}