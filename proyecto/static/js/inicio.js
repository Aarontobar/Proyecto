document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.carousel');
    let isDragging = false;
    let startPosition = 0;
    let currentTranslate = 0;

    carousel.addEventListener('mousedown', (e) => {
        isDragging = true;
        startPosition = e.clientX - carousel.offsetLeft;
        currentTranslate = 0;

        carousel.style.transition = 'none';
    });

    carousel.addEventListener('mouseup', () => {
        isDragging = false;
        const movedBy = e.clientX - startPosition;

        if (movedBy < -100) {
            // Move to next slide
        } else if (movedBy > 100) {
            // Move to previous slide
        }

        carousel.style.transition = 'transform 0.5s ease';
        carousel.style.transform = `translateX(${currentTranslate}px)`;
    });

    carousel.addEventListener('mouseleave', () => {
        isDragging = false;
        carousel.style.transition = 'transform 0.5s ease';
        carousel.style.transform = `translateX(${currentTranslate}px)`;
    });

    carousel.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const currentPosition = e.clientX - startPosition;
            currentTranslate = currentPosition;
            carousel.style.transform = `translateX(${currentTranslate}px)`;
        }
    });
});