
function showDemoPopup() {
    const popup = document.getElementById('demoPopup');
    popup.style.display = 'flex';
}

function closePopup() {
    const popup = document.getElementById('demoPopup');
    popup.style.display = 'none';
}


function submitDemo() {

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const company = document.getElementById('company').value;
    const phone = document.getElementById('phone').value;
    
    if (!name || !email || !company || !phone) {
        alert('Please fill in all fields!');
        return;
    }

    
    alert('Thank you for your interest! Our team will contact you shortly.');
    closePopup();
}


