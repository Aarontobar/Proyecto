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
    var patenteField = document.getElementById('transfer-patente');
    
    patenteField.value = transferPatente; // Establece la patente en un campo oculto
    formContainer.style.display = 'block'; // Muestra el contenedor del formulario
    formContainer.scrollIntoView({ behavior: 'smooth' }); // Desplaza la vista al formulario
}