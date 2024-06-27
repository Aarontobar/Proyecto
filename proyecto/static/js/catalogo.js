document.addEventListener('DOMContentLoaded', function() {
    var showMoreBtns = document.querySelectorAll('.mas_info_btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.closest('.transfer-card');
            card.classList.toggle('expanded');
        });
    });
});

function showReservationForm(event, transferPatente) {
    event.preventDefault();
    var formContainer = document.getElementById('reservation-form-container');
    var form = document.getElementById('reservation-form');
    console.log('Formulario de reserva mostrado para el transfer ID:', transferPatente);
    var patenteField = document.getElementById('transfer-patente');
    
    patenteField.value = transferPatente; 
    formContainer.style.display = 'block'; 
    formContainer.scrollIntoView({ behavior: 'smooth' }); 
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const reservaTransferId = urlParams.get('reserva_transfer_id');
    if (reservaTransferId) {
        const formContainer = document.getElementById('reservation-form-container');
        console.log('Formulario', reservaTransferId);
        if (formContainer) {
            formContainer.style.display = 'block';
            formContainer.scrollIntoView({ behavior: 'smooth' });

            console.log('Formulario de reserva mostrado para el transfer ID:', reservaTransferId);
        }
    }
});