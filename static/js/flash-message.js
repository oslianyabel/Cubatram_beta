document.addEventListener('DOMContentLoaded', function () {
    const flash = document.getElementById('flash-message');
    if (flash) {
        setTimeout(() => {
            flash.style.transition = 'opacity 0.5s';
            flash.style.opacity = 0;
            setTimeout(() => flash.remove(), 500);
        }, 3000);
    }
});
