document.addEventListener('DOMContentLoaded', function() {
    var showMoreBtns = document.querySelectorAll('.mas_info_btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.closest('.transfer-card');
            card.classList.toggle('expanded');
        });
    });
});

function showReservationForm(event, transferPatente, capacidad) {
    event.preventDefault();
    var formContainer = document.getElementById('reservation-form-container');
    var form = document.getElementById('reservation-form');
    var capacidades = document.getElementById('cantidad_asientos');
    console.log('Formulario de reserva mostrado para el transfer ID:', transferPatente);
    var patenteField = document.getElementById('transfer-patente');
    
    patenteField.value = transferPatente; 
    formContainer.style.display = 'block'; 
    formContainer.scrollIntoView({ behavior: 'smooth' }); 
    capacidades.setAttribute('max', capacidad);
}

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const reservaTransferId = urlParams.get('reserva_transfer_id');
    const capacidad = urlParams.get('capacidad')
    
    if (reservaTransferId) {
        const formContainer = document.getElementById('reservation-form-container');
        console.log('Formulario', reservaTransferId);
        var capacidades = document.getElementById('cantidad_asientos');
        if (formContainer) {
            formContainer.style.display = 'block';
            formContainer.scrollIntoView({ behavior: 'smooth' });
            capacidades.setAttribute('max', capacidad);

            console.log('Formulario de reserva mostrado para el transfer ID:', reservaTransferId);
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const zonaSelect = document.getElementById('zona');
    const comunaSelect = document.getElementById('comuna');
    const transfersContainer = document.getElementById('transfers');

    function checkSelections() {
        if (zonaSelect.value || comunaSelect.value) {
            transfersContainer.style.display = '';
        } else {
            transfersContainer.style.display = 'none';
        }
    }

    checkSelections();
});