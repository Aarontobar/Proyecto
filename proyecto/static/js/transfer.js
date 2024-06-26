document.addEventListener('DOMContentLoaded', function() {
    var showMoreBtns = document.querySelectorAll('.mas_info_btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.closest('.transfer-card');
            card.classList.toggle('expanded');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var toggleBtn = document.getElementById('toggle-filter-btn');
    var filterForm = document.getElementById('filter-form');

    toggleBtn.addEventListener('click', function() {
        filterForm.classList.toggle('hidden');
    });
});