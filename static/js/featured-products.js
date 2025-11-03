document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('featuredProductsSlider');

    if (!slider) {
        return;
    }

    // Sonsuz döngü için içeriği kopyala
    const originalContent = slider.innerHTML;
    slider.innerHTML = originalContent + originalContent;
    
    // Yeni linkleri al (kopyalanan içerik dahil)
    const productLinks = slider.querySelectorAll('.product-link');
    
    // Orijinal içeriğin genişliğini hesapla
    let originalWidth = 0;
    let isScrolling = false;
    
    function calculateOriginalWidth() {
        // En basit ve doğru yöntem: slider'ın toplam genişliğinin yarısı
        // Çünkü içeriği ikiye böldük (orijinal + kopya)
        originalWidth = slider.scrollWidth / 2;
        
        // Alternatif: İkinci setin başlangıç pozisyonunu kullan (daha doğru)
        const cards = slider.querySelectorAll('.featured-product-card');
        if (cards.length > 0) {
            const midIndex = Math.floor(cards.length / 2);
            if (cards[midIndex]) {
                const midCardLeft = cards[midIndex].offsetLeft;
                if (midCardLeft > 0) {
                    originalWidth = midCardLeft;
                }
            }
        }
    }
    
    // Sayfa yüklendikten sonra genişliği hesapla
    setTimeout(function() {
        calculateOriginalWidth();
        // Scroll pozisyonunu orijinal içeriğin başlangıcına ayarla
        slider.scrollLeft = 0;
    }, 100);
    
    // Scroll event listener - sonsuz döngü için
    slider.addEventListener('scroll', function() {
        if (isScrolling) return;
        
        // Eğer klonun başına geldiysek (orijinal genişliğe ulaştıysak)
        if (slider.scrollLeft >= originalWidth) {
            isScrolling = true;
            // Sessizce orijinal başlangıca dön (animasyon yok)
            slider.scrollLeft = slider.scrollLeft - originalWidth;
            setTimeout(function() {
                isScrolling = false;
            }, 50);
        }
        // Eğer geriye kaydırıyorsak ve başa geldiysek
        else if (slider.scrollLeft <= 0 && originalWidth > 0) {
            isScrolling = true;
            // Orijinal sona git
            slider.scrollLeft = originalWidth;
            setTimeout(function() {
                isScrolling = false;
            }, 50);
        }
    });

    // Drag/Swipe functionality
    let isDown = false;
    let startX;
    let scrollLeft;

    // Otomatik kaydırma DEVRE DIŞI - performans için kaldırıldı
    let autoScrollInterval = null;
    let isPaused = false;
    // const scrollSpeed = 1; // Piksel cinsinden kaydırma hızı
    // const scrollDelay = 15; // Her X ms'de bir kaydır
    
    function startAutoScroll() {
        // Auto-scroll devre dışı - performans için
        return;
    }
    
    function stopAutoScroll() {
        if (autoScrollInterval) {
            clearInterval(autoScrollInterval);
            autoScrollInterval = null;
        }
    }
    
    // Hover durumunda duraklat
    slider.addEventListener('mouseenter', function() {
        isPaused = true;
    });
    
    slider.addEventListener('mouseleave', function() {
        isPaused = false;
        // Drag sırasında mouseleave olursa drag'i sonlandır
        if (isDown) {
            isDown = false;
            slider.classList.remove('dragging');
            slider.style.cursor = 'grab';
        }
    });

    slider.addEventListener('mousedown', function(e) {
        isDown = true;
        slider.classList.add('dragging');
        startX = e.pageX - slider.offsetLeft;
        scrollLeft = slider.scrollLeft;
        slider.style.cursor = 'grabbing';
    });

    slider.addEventListener('mouseup', function() {
        isDown = false;
        slider.classList.remove('dragging');
        slider.style.cursor = 'grab';
    });

    slider.addEventListener('mousemove', function(e) {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - slider.offsetLeft;
        const walk = (x - startX) * 2; // Scroll hızı
        slider.scrollLeft = scrollLeft - walk;
    });

    // Touch events for mobile
    let touchStartX;
    let touchScrollLeft;

    slider.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].pageX - slider.offsetLeft;
        touchScrollLeft = slider.scrollLeft;
    }, { passive: true });

    slider.addEventListener('touchmove', function(e) {
        if (!touchStartX) return;
        const touchX = e.touches[0].pageX - slider.offsetLeft;
        const walk = (touchX - touchStartX) * 2;
        slider.scrollLeft = touchScrollLeft - walk;
    }, { passive: true });

    slider.addEventListener('touchend', function() {
        touchStartX = null;
    });

    // Ürün linklerine tıklama - özel sayfaya yönlendirme
    productLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            const slug = this.getAttribute('data-slug');
            window.location.href = '/urun/' + slug + '/';
        });
    });


    // Klavye navigasyonu (opsiyonel)
    slider.setAttribute('tabindex', '0');
    slider.addEventListener('keydown', function(e) {
        const card = slider.querySelector('.featured-product-card');
        if (!card) return;
        const cardWidth = card.offsetWidth;
        const gap = 30;
        
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            slider.scrollBy({
                left: -(cardWidth + gap),
                behavior: 'smooth'
            });
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            slider.scrollBy({
                left: (cardWidth + gap),
                behavior: 'smooth'
            });
        }
    });
    
    // Resize event - genişliği yeniden hesapla
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            calculateOriginalWidth();
        }, 250);
    });
});

