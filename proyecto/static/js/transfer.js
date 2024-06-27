document.addEventListener('DOMContentLoaded', function() {
    var showMoreBtns = document.querySelectorAll('.mas_info_btn');

    showMoreBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var card = this.closest('.transfer-card');
            card.classList.toggle('expanded');
        });
    });
});
