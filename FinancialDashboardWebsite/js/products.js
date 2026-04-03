
// Product Demo Modal
function showProductDemo(productName) {
    const demoMODEL = document.getElementById('demoMODEL');
    const demoTitle = document.getElementById('demoTitle');
    const demoVideo = document.getElementById('ActualVideo');
    
    demoTitle.textContent = productName + ' Demo';
    
    let videoId = '';
    
    if (productName === 'BajwaSales Dashboard') {
        videoId = 'U1-tNfr9P8k';
    } else if (productName === 'ForecastPro') {
        videoId = 'U1-tNfr9P8k';
    } else if (productName === 'PerformanceAnalyzer') {
        videoId = 'U1-tNfr9P8k';
    } else if (productName === 'CustomerInsights') {
        videoId = 'U1-tNfr9P8k';
    }
    
    demoVideo.src = 'https://www.youtube.com/embed/' + videoId;
    
    demoMODEL.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

// Contact Form Modal
function showContactForm() {
    const contactModal = document.getElementById('contactModal');
    contactModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    
    if (modalId === 'demoMODEL') {
        const demoVideo = document.getElementById('demoVideo');
        demoVideo.src = '';
    }
}

function submitContactForm() {
    const name = document.getElementById('contactName').value;
    const email = document.getElementById('contactEmail').value;
    const company = document.getElementById('contactCompany').value;
    const phone = document.getElementById('contactPhone').value;
    const message = document.getElementById('contactMessage').value;
    
    if (!name || !email || !company || !phone || !message) {
        alert('Please fill in all fields!');
        return;
    }
    
    alert('Thank you for your inquiry! Our sales team will contact you shortly.');
    closeModal('contactModal');
}
