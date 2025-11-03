document.addEventListener('DOMContentLoaded', function() {
    let nextButton = document.getElementById('next');
    let prevButton = document.getElementById('prev');
    let carousel = document.querySelector('.carousel');
    let listHTML = document.querySelector('.carousel .list');
    let seeMoreButtons = document.querySelectorAll('.seeMore');
    let backButton = document.getElementById('back');

    if (!nextButton || !prevButton || !carousel || !listHTML || !backButton) {
        return;
    }

    // Sadece görünür olan modeli oynat, diğerlerini durdur
    function updateModelPlayback() {
        let items = document.querySelectorAll('.carousel .list .item');
        items.forEach((item, index) => {
            let iframe = item.querySelector('iframe');
            if (!iframe) return;
            
            let currentSrc = iframe.src;
            // Base URL'i al (parametreler olmadan)
            let baseUrl = currentSrc.split('?')[0];
            // Titlebar'ı gizlemek için sabit parametreler
            let hideUiParams = 'ui_infos=0&ui_watermark=0';
            
            // 2. item (index 1) görünür olan modeldir
            if (index === 1) {
                // Görünür model için autostart ekle
                if (!currentSrc.includes('autostart=1')) {
                    iframe.src = baseUrl + '?' + hideUiParams + '&autostart=1&autospin=0.2';
                }
            } else {
                // Görünmeyen modeller için autostart=0 yap (durdur)
                // Mevcut parametreleri temizle ve sadece autostart=0 ekle
                if (currentSrc.includes('autostart=1') || !currentSrc.includes('autostart=0')) {
                    iframe.src = baseUrl + '?' + hideUiParams + '&autostart=0';
                }
            }
        });
    }

    // İlk yüklemede sadece görünür modeli oynat
    setTimeout(updateModelPlayback, 500);

    nextButton.onclick = function(){
        showSlider('next');
    }
    prevButton.onclick = function(){
        showSlider('prev');
    }
    let unAcceppClick;
    const showSlider = (type) => {
        nextButton.style.pointerEvents = 'none';
        prevButton.style.pointerEvents = 'none';

        carousel.classList.remove('next', 'prev');
        let items = document.querySelectorAll('.carousel .list .item');
        if(type === 'next'){
            listHTML.appendChild(items[0]);
            carousel.classList.add('next');
        }else{
            listHTML.prepend(items[items.length - 1]);
            carousel.classList.add('prev');
        }
        
        // Carousel değiştiğinde model oynatma durumunu güncelle
        setTimeout(updateModelPlayback, 100);
        
        clearTimeout(unAcceppClick);
        unAcceppClick = setTimeout(()=>{
            nextButton.style.pointerEvents = 'auto';
            prevButton.style.pointerEvents = 'auto';
            // Animasyon bittikten sonra tekrar güncelle
            updateModelPlayback();
        }, 2000)
    }
    seeMoreButtons.forEach((button) => {
        button.onclick = function(){
            carousel.classList.remove('next', 'prev');
            carousel.classList.add('showDetail');
            // Detail görünümünde de model oynatma durumunu güncelle
            setTimeout(updateModelPlayback, 100);
        };
    });
    backButton.onclick = function(){
        carousel.classList.remove('showDetail');
        // Detail'den çıkınca model oynatma durumunu güncelle
        setTimeout(updateModelPlayback, 100);
    }
});

