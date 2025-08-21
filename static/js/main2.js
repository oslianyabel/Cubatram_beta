document.addEventListener('DOMContentLoaded', function () {
    const slides = document.querySelectorAll('.header-slide');
    let currentSlide = 0;
    const slideInterval = 7000; // 7 segundos

    // Estilos iniciales para desplazamiento
    slides.forEach((slide, idx) => {
        slide.style.position = 'absolute';
        slide.style.top = 0;
        slide.style.left = 0;
        slide.style.width = '100%';
        slide.style.height = '100%';
        slide.style.transition = 'transform 1s cubic-bezier(0.77,0,0.18,1)';
        slide.style.transform = `translateX(${idx === 0 ? 0 : 100}%)`;
        slide.style.opacity = 1;
        slide.style.zIndex = idx === 0 ? 2 : 1;
    });

    function nextSlide() {
        // Si ya estamos en la última imagen, no mover nada y detener el intervalo
        if (currentSlide >= slides.length - 1) {
            clearInterval(slideTimer);
            return;
        }
        const prevSlide = slides[currentSlide];
        prevSlide.style.zIndex = 1;
        prevSlide.style.transform = 'translateX(-100%)';
        currentSlide++;
        const newSlide = slides[currentSlide];
        newSlide.style.transform = 'translateX(0)';
        newSlide.style.zIndex = 2;
        // Reposicionar el resto a la derecha
        slides.forEach((slide, idx) => {
            if (idx !== currentSlide && slide !== prevSlide) {
                slide.style.transform = 'translateX(100%)';
                slide.style.zIndex = 1;
            }
        });
    }
    // Iniciar el carrusel
    let slideTimer = setInterval(nextSlide, slideInterval);
    // Pausar al pasar el mouse
    const carousel = document.querySelector('.header-carousel');
    carousel.addEventListener('mouseenter', () => clearInterval(slideTimer));
    carousel.addEventListener('mouseleave', () => {
        slideTimer = setInterval(nextSlide, slideInterval);
    });

    const findTourBtn = document.getElementById('find-tour-btn');
    const destinationSelect = document.getElementById('destination-select');
    const categorySelect = document.getElementById('category-select');

    // Mostrar los filter-btn en mobile al hacer click en Find Tour por primera vez
    let filterBtnsShown = false;
    findTourBtn.addEventListener('click', function (e) {
        // Solo para pantallas <= 490px
        if (window.innerWidth <= 490 && !filterBtnsShown) {
            e.preventDefault();
            const filterBtns = document.querySelectorAll('.filter-btn');
            filterBtns.forEach(btn => btn.classList.add('show'));
            filterBtnsShown = true;
            // Animar el botón Find Tour
            findTourBtn.classList.add('moved');
            // Scroll suave hacia los filtros
            if (filterBtns.length > 0) {
                setTimeout(() => {
                    filterBtns[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            }
            return;
        }

        e.preventDefault();
        const destinationSlug = destinationSelect.value;
        const categorySlug = categorySelect.value;
        if (destinationSlug && categorySlug) {
            const url = `/tours/destination/${destinationSlug}/category/${categorySlug}/`;
            window.location.href = url;
        } else {
            alert('Please select both a destination and a category');
        }
    });
});