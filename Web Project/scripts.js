document.addEventListener('DOMContentLoaded', () => {
    const sliders = document.querySelectorAll('.slider-container');

    sliders.forEach(slider => {
        const productSlider = slider.querySelector('.product-slider');
        const leftBtn = slider.querySelector('.left-btn');
        const rightBtn = slider.querySelector('.right-btn');

        let scrollAmount = 0;
        const scrollStep = 250;

        leftBtn.addEventListener('click', () => {
            scrollAmount -= scrollStep;
            if (scrollAmount < 0) scrollAmount = 0;
            productSlider.style.transform = `translateX(-${scrollAmount}px)`;
        });

        rightBtn.addEventListener('click', () => {
            const maxScroll = productSlider.scrollWidth - slider.offsetWidth;
            scrollAmount += scrollStep;
            if (scrollAmount > maxScroll) scrollAmount = maxScroll;
            productSlider.style.transform = `translateX(-${scrollAmount}px)`;
        });
    });
});
